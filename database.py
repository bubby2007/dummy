from pymongo import MongoClient, ASCENDING
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from datetime import datetime, timedelta
from utils.encryption import Encryptor
from utils.config import (
    MONGO_URI, MONGO_OPTIONS, DATABASE_NAME, 
    COLLECTION_NAME, ENCRYPTION_KEY
)
import streamlit as st

class Database:
    def __init__(self):
        try:
            self.client = MongoClient(MONGO_URI, **MONGO_OPTIONS)
            self.client.admin.command('ping')
            
            self.db = self.client[DATABASE_NAME]
            self.collection = self.db[COLLECTION_NAME]
            self.sessions = self.db['survey_sessions']
            self.encryptor = Encryptor(ENCRYPTION_KEY)
            
            # Create indices
            self.collection.create_index([("session_id", ASCENDING)])
            self.collection.create_index([("expires_at", ASCENDING)])
            self.sessions.create_index([("expires_at", ASCENDING)])
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            st.error("MongoDB Connection Error. Please check your connection.")
            raise Exception(f"MongoDB Connection Error: {str(e)}")

    def store_response(self, response_data, session_id):
        """Store encrypted response with session ID"""
        try:
            # Get session expiry time
            session = self.sessions.find_one({'session_id': session_id})
            if not session:
                raise Exception("Invalid session")
                
            encrypted_data = self.encryptor.encrypt_data(response_data)
            
            document = {
                'data': encrypted_data,
                'session_id': session_id,
                'created_at': datetime.utcnow(),
                'expires_at': session['expires_at']
            }
            
            result = self.collection.insert_one(document)
            return result
            
        except Exception as e:
            st.error(f"Error storing data: {str(e)}")
            raise

    def get_session_responses(self, session_id):
        """Get all responses for a session"""
        try:
            responses = self.collection.find({
                'session_id': session_id,
                'expires_at': {'$gt': datetime.utcnow()}
            })
            return list(responses)
        except Exception as e:
            st.error(f"Error retrieving responses: {str(e)}")
            return []

    def cleanup_expired_sessions(self):
        """Remove expired sessions and their responses"""
        try:
            current_time = datetime.utcnow()
            
            # Find expired sessions
            expired_sessions = self.sessions.find({
                'expires_at': {'$lte': current_time}
            })
            
            # Delete responses for expired sessions
            for session in expired_sessions:
                self.collection.delete_many({
                    'session_id': session['session_id']
                })
            
            # Delete expired sessions
            self.sessions.delete_many({
                'expires_at': {'$lte': current_time}
            })
            
        except Exception as e:
            st.warning(f"Error during cleanup: {str(e)}")

    def get_response_stats(self):
        """Get basic statistics about responses"""
        try:
            current_time = datetime.utcnow()
            total_responses = self.collection.count_documents({
                'expires_at': {'$gt': current_time}
            })
            
            return {
                'total_responses': total_responses,
                'last_updated': current_time
            }
        except Exception as e:
            st.error(f"Error getting stats: {str(e)}")
            return {'total_responses': 0, 'last_updated': current_time}

    def __del__(self):
        try:
            self.client.close()
        except:
            pass
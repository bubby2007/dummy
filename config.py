from dotenv import load_dotenv
import os

load_dotenv()

# MongoDB Configuration
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
MONGO_OPTIONS = {
    'serverSelectionTimeoutMS': 5000,
    'connectTimeoutMS': 10000,
    'retryWrites': True,
    'w': 'majority'
}
DATABASE_NAME = 'mental_health_survey_db'
COLLECTION_NAME = 'responses'

# Encryption Configuration
DEFAULT_KEY = 'default_encryption_key_12345'.ljust(32, '0')
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY', DEFAULT_KEY)

# Session Configuration
SESSION_DURATION_MINUTES = 30  # Session and data retention duration
BASE_URL = os.getenv('BASE_URL', 'http://localhost:8501/mental_health')
import streamlit as st
import sys
from pathlib import Path
from datetime import datetime, timedelta
from utils.database import Database
from utils.config import SESSION_DURATION_MINUTES
from utils.session_manager import SessionManager

# Set page configuration
st.set_page_config(
    page_title="Student Wellness Survey - Hushlytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS styles consistent with Academic_Integrity.py
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

    :root {
        --primary-font: 'Poppins', sans-serif;
        --white: #ffffff;
        --black: #000000;
    }

    body {
        font-family: var(--primary-font);
    }

    h1, h2, h3, .title {
        font-family: var(--primary-font);
        font-weight: 700;
        letter-spacing: 0.5px;
        color: var(--black);
    }

    .subtitle {
        font-family: var(--primary-font);
        font-weight: 400;
        color: #555;
        margin-bottom: 20px;
    }

    .form-container {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    .success-message {
        font-family: var(--primary-font);
        color: #2d3748;
        font-weight: 600;
        margin-top: 10px;
    }

    .stButton button {
        font-family: var(--primary-font);
        font-size: 16px;
        font-weight: 600;
        color: var(--white);
        background-color: var(--black);
        border-radius: 10px;
        padding: 10px 20px;
        border: none;
        transition: transform 0.1s ease-in-out, background-color 0.2s;
    }

    .stButton button:hover {
        transform: scale(1.05);
        background-color: #333;
    }

    .stButton button:focus {
        color: var(--white) !important;
        outline: none;
    }
    </style>
""", unsafe_allow_html=True)

def generate_survey_link():
    """Generate a new survey session link"""
    session_manager = SessionManager(SESSION_DURATION_MINUTES)
    link, expiry_time = session_manager.generate_session_link()
    
    st.markdown("### 🔗 Survey Session Link")
    st.code(link, language="text")
    
    # Display countdown timer
    time_remaining = expiry_time - datetime.utcnow()
    minutes_remaining = int(time_remaining.total_seconds() / 60)
    
    st.markdown(f"### ⏱️ Session expires in: {minutes_remaining} minutes")
    st.warning(f"""
        - This link will be active for {SESSION_DURATION_MINUTES} minutes
        - Multiple responses can be collected during this time
        - All responses will be automatically deleted after session expiry
    """)
    
    if st.button("Copy Link", key="copy_link"):
        st.success("Link copied to clipboard!")
        
    return link

def display_survey_form(db, session_id):
    """Display the survey form and handle submissions"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<div class='form-container'>", unsafe_allow_html=True)
        
        with st.form("student_wellness_survey", clear_on_submit=True):
            st.subheader("Demographics")
            age = st.number_input("Age:", min_value=16, max_value=100, step=1)
            gender = st.selectbox("Gender:", ["Male", "Female", "Non-binary", "Other", "Prefer not to say"])
            academic_year = st.selectbox("Academic Year:", ["Freshman", "Sophomore", "Junior", "Senior", "Graduate"])
            living_situation = st.selectbox("Living Situation:", ["On-campus", "Off-campus"])
            employment_status = st.selectbox("Employment Status:", ["Unemployed", "Part-time", "Full-time"])
            
            st.markdown("---")
            
            st.subheader("Academic & Mental Health Factors")
            academic_dishonesty = st.selectbox("Experiences with academic dishonesty:", ["None", "Minor", "Severe"])
            perceived_pressure = st.slider("Perceived pressure to perform well (1-5):", 1, 5, 3)
            workload_stress = st.slider("Workload stress (1-5):", 1, 5, 3)
            depression_score = st.number_input("Depression score (PHQ-9 items):", min_value=0, max_value=27, step=1)
            anxiety_score = st.number_input("Anxiety score (GAD-7 items):", min_value=0, max_value=21, step=1)
            
            st.markdown("---")
            
            st.subheader("Lifestyle Factors")
            study_hours = st.number_input("Study Hours per Week:", min_value=0, max_value=100, step=1)
            academic_pressure = st.slider("Academic pressure (1-5):", 1, 5, 3)
            exercise_frequency = st.selectbox("Exercise Frequency:", ["Never", "Rarely", "Regularly"])
            meditation = st.selectbox("Meditation/Mindfulness Practice:", ["Never", "Occasionally", "Regularly"])
            social_activities = st.selectbox("Social Activities Level:", ["Low", "Moderate", "High"])
            
            st.markdown("---")
            
            st.subheader("Mental Health Support & Resources")
            professional_help = st.selectbox("Professional Help Utilization:", ["Never", "Occasionally", "Regularly"])
            access_counseling = st.selectbox("Access to Counseling:", ["Yes", "No", "Unsure"])
            support_network = st.slider("Support Network Rating (1-10):", 1, 10, 5)
            campus_resources = st.selectbox("Knowledge of Campus Resources:", ["Poor", "Moderate", "Good", "Excellent"])
            barriers_help = st.selectbox("Barriers to Seeking Help:", ["None", "Cost", "Availability", "Other"])
            
            st.info("🔒 Your responses are encrypted and will be deleted after the session expires")
            submitted = st.form_submit_button("Submit Survey")
            
            if submitted:
                try:
                    response_data = {
                        'age': age,
                        'gender': gender,
                        'academic_year': academic_year,
                        'living_situation': living_situation,
                        'employment_status': employment_status,
                        'academic_dishonesty': academic_dishonesty,
                        'perceived_pressure': perceived_pressure,
                        'workload_stress': workload_stress,
                        'depression_score': depression_score,
                        'anxiety_score': anxiety_score,
                        'study_hours': study_hours,
                        'academic_pressure': academic_pressure,
                        'exercise_frequency': exercise_frequency,
                        'meditation': meditation,
                        'social_activities': social_activities,
                        'professional_help': professional_help,
                        'access_counseling': access_counseling,
                        'support_network': support_network,
                        'campus_resources': campus_resources,
                        'barriers_help': barriers_help,
                        'submitted_at': datetime.utcnow().isoformat()
                    }
                    
                    db.store_response(response_data, session_id)
                    st.success("✨ Thank you for completing the survey!")
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"Error submitting survey: {str(e)}")
                    
        st.markdown("</div>", unsafe_allow_html=True)

# Add other functions (display_responses, main, etc.) following the same pattern.

import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Sexual Health & Awareness - Hushlytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS styles consistent with Academic_Integrity.py
st.markdown(
    """
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

    .resource-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }

    .resource-title {
        font-family: var(--primary-font);
        font-weight: 600;
        color: var(--black);
    }

    .upload-section {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
    }

    .upload-title {
        font-family: var(--primary-font);
        font-weight: 600;
        color: var(--black);
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
    """,
    unsafe_allow_html=True
)
st.sidebar.image("logo.png", use_container_width=True)  # Ensure logo is at the bottom

# Main content
st.markdown('<div class="main">', unsafe_allow_html=True)

# Back button with consistent style
if st.button("← Back to Dashboard"):
    st.query_params = {"page": "Home.py"}

# Title and description
st.markdown("<h1 class='title'>Sexual Health & Awareness</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='subtitle'>Promote comprehensive sexual health education and awareness through confidential feedback.</p>",
    unsafe_allow_html=True
)

# Resource section
st.markdown(
    """
    <div class="resource-card">
        <h2 class="resource-title">Useful Resources</h2>
        <p style="color: #4a5568; margin-bottom: 1rem;">
            Access comprehensive sexual health resources, guidelines, and best practices for conducting surveys and analyzing data responsibly.
        </p>
        <a href="https://sample.com" target="_blank" class="resource-link">
            Access Resources →
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

# Upload section
st.markdown('<div class="upload-section">', unsafe_allow_html=True)
st.markdown('<h2 class="upload-title">Upload Your Dataset</h2>', unsafe_allow_html=True)
st.markdown(
    '<p style="color: #718096; margin-bottom: 2rem;">Upload your sexual health awareness survey data for analysis while maintaining complete privacy.</p>',
    unsafe_allow_html=True
)

# File upload with custom styling
dataset = st.file_uploader("Choose a file", type=["csv", "xlsx", "json"])

if dataset is not None:
    st.markdown(
        '<div class="success-message">✨ Dataset uploaded successfully! Ready for analysis.</div>',
        unsafe_allow_html=True
    )

st.markdown('</div>', unsafe_allow_html=True)  # Close upload section
st.markdown('</div>', unsafe_allow_html=True)  # Close main container

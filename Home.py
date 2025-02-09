import streamlit as st

# Set page configuration
st.set_page_config(page_title="VeraCrypt", layout="wide")
st.sidebar.image("logo.png", use_container_width=True) 

# Updated CSS for styling
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

    .category-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        min-height: 200px;
        transition: transform 0.2s ease-in-out;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        margin-bottom: 20px;
    }

    .category-card:hover {
        transform: scale(1.03);
    }

    .category-description {
        font-family: var(--primary-font);
        font-weight: 400;
        color: #555;
        margin-bottom: 20px;
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

# Main content
st.title("Welcome to VeraCrypt")
st.write("Discover meaningful insights through creating anonymous surveys for people around you.")

# Category sections
categories = {
    "Mental Health & Well-being": "Gain valuable insights into mental health trends and support needs through anonymous feedback.",
    "Academic Integrity & Performance": "Evaluate academic honesty practices and identify areas for improving educational outcomes.",
    "Socioeconomic Status & Financial Hardship": "Understand economic challenges and develop targeted support strategies for your community.",
    "Diversity, Equality & Inclusion": "Assess inclusivity initiatives and gather insights to create a more equitable environment.",
    "Sexual Health & Awareness": "Promote comprehensive sexual health education and awareness through confidential feedback.",
    "Substance Use & Risk Behavior": "Address substance use patterns and develop effective prevention strategies."
}

# Align categories in rows of 2 for a cleaner layout
cols = st.columns(2)
for index, (title, description) in enumerate(categories.items()):
    col = cols[index % 2]
    with col:
        st.markdown(f"""
            <div class='category-card'>
                <h3>{title}</h3>
                <p class='category-description'>{description}</p>
            </div>
        """, unsafe_allow_html=True)
        st.button(f"Explore {title}", key=f"btn_{index}")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center;'>🔒 All surveys are anonymous and encrypted.</p>", unsafe_allow_html=True)

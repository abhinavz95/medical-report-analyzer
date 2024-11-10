import streamlit as st
from src.pipeline import Pipeline
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Set page configuration at the very start
st.set_page_config(page_title=" Medical Report Analyzer", page_icon="*")

# Retrieve the API key from environment variables
api_key = os.getenv("GOOGLE_API_KEY")

# Add a sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go to", ["Medical Report Analyzer", "About Me"])

# Cache the Pipeline to avoid reloading/re-initializing on every rerun
@st.cache_resource
def load_pipeline():
    pipeline = Pipeline()  # Ensure this is creating an instance
    pipeline.load_model()  # Make sure model is loaded when pipeline is created
    return pipeline

# Initialize the pipeline once and reuse it
pipeline = load_pipeline()  # This should be an instance now

# Medical Report Analyzer Page
if page == "Medical Report Analyzer":
    st.markdown("<h1 style='text-align: center;'>Medical Report Analyzer 🔎</h1>", unsafe_allow_html=True)
    st.caption("Health Insights Based on The Lab Reports")

    # Check if API key is available
    if not api_key:
        st.error("API key not found. Please add it to the .env file.")
    else:
        # File uploader for lab reports
        file = st.file_uploader(label="Upload Lab Report", type=["PDF", "JPG", "PNG", "JPEG"])

        # Button to process the report
        if st.button("Process"):
            if file is not None:
                file_type = file.name.split(".")[-1].lower()
                # Pass file and file_type as arguments
                response = pipeline.process(file, file_type)
                st.write(response)  # Display the processed response
            else:
                st.warning("Please upload a file.", icon="⚠️")

# About Me Page
elif page == "About Me":
    st.markdown("<h1 style='text-align: center;'>About Me 🧑‍💻</h1>", unsafe_allow_html=True)
    
    # Add information about the developer
    st.write("### Developer Profile")
    st.write("""
    **Name**:   abhinav pal
    **Role**: ML & AI Enthusiast  
    **Skills**:  
    - Machine Learning  
    - Natural Language Processing  
    - Large Language Models

    **About Me**:  
    I'm a passionate engineering student with experience in AI and machine learning. This project is aimed at simplifying the process of understanding medical reports using cutting-edge language models and AI technology.  
    """)

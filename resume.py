import streamlit as st
import google.generativeai as genai
import PyPDF2 as pdf
import webbrowser
import json
import subprocess
import time
import requests

# Configure Streamlit page settings
st.set_page_config(
    page_title="Smart ATS",
    page_icon="👨‍💼",
    layout="centered",
)


# Function to configure Gemini AI model with the provided API key
def configure_gemini_api(api_key):
    genai.configure(api_key=api_key)


# Replace with your actual API key
API_KEY = 'AIzaSyDTenTn5lavhor_cot1odUWBJmScuR6G30'
configure_gemini_api(API_KEY)


# Function to get response from Gemini AI
def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text


# Function to extract text from uploaded PDF file
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text


# Prompt Template
input_prompt = """
Hey Act Like a skilled or very experienced ATS (Application Tracking System)
with a deep understanding of the tech field, software engineering, data science, data analyst
and big data engineering. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide the 
best assistance for improving the resumes. Assign the percentage Matching based 
on JD and the missing keywords with high accuracy and also provide suggestions to improve the resume of this 
particular resume and also suggest courses or website links to improve. Also tell if the resume is Ats friendly or 
not and tell the percentage.
resume:{text}
description:{jd}

I want the response in one single string having the structure
{{"JD Match":"%","MissingKeywords":[],"Profile Summary":"","Suggestions":"","Course Suggestions":"","ATS-Friendly":""}}
"""

## Streamlit app
st.title("Resume Matcher ATS")

# Left panel for AI mock tests
st.sidebar.title("AI Mock Tests")


# Function to run the Flask application
def run_flask_app():
    st.write("Starting Flask application...")

    process = subprocess.Popen(["python", "mcq/final_test.py"])
    webbrowser.open_new_tab("http://localhost:5000/")
    time.sleep(5)  # Waiting for Flask app to start (adjust as needed)
    if process.poll() is None:
        st.write("Flask application is running.")
        st.write(f"Open this URL in your browser: http://localhost:5000/technical_test")


# Button to launch the Flask application
if st.sidebar.button("AI Mock Technical Test"):
    run_flask_app()
if st.sidebar.button("AI Mock Aptitude Test"):
    run_flask_app()
# Main content area
st.markdown("---")  # Horizontal line for separation

jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the PDF")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt.format(text=text, jd=jd))



        try:
            parsed_response = json.loads(response)
            st.subheader("Response:")
            for key, value in parsed_response.items():
                st.write(f"**{key}:** {value}")
        except json.JSONDecodeError as e:
            st.error(f"JSON Decode Error: {e}")
            st.error("Raw response might not be in JSON format.")

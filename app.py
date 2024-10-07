import streamlit as st
import requests
import base64

# Configure Streamlit page settings
st.set_page_config(
    page_title="Resume Matcher ATS",
    page_icon="📄",
    layout="centered",
)

# Streamlit app title and description
st.title("Resume Matcher ATS")
st.markdown("Upload your resume PDF and provide the job description to get evaluation results.")

# Function to convert file to base64
def convert_file_to_base64(file):
    file_content = file.read()
    return base64.b64encode(file_content).decode('utf-8')

# Job Responsibilities and Requirements
job_responsibilities = """
Create features in Angular 2+ while working with product managers, engineers, and designers
Develop reusable and effective front-end code to improve the user experience for the company
Structure each project's deliverables, deadlines, and priority
Construct and manage integration and unit tests
Quickly fix faults and come up with strong solutions for challenging issues
Observe established procedures to keep the organization's state intact
"""

job_requirements = """
Bachelor’s/Master’s degree in Engineering, Computer Science (or equivalent experience)
At least 5+ years of relevant experience as a front-end engineer
5+ years of working experience with JavaScript and Angular 2+
Demonstrable experience working with Redux style state management NgRx, TypeScript, and RxJs
Comprehensive understanding of HTML and CSS, covering ideas like accessibility, cross-browser compatibility, layout, and specificity
Prior experience mentoring coworkers on innovative ways to hone their technical expertise
Be an effective self-starter who is operationally focused and a problem-solver
Great interpersonal and team building skills
Excellent English communication skills, both spoken and written
"""

# Streamlit widgets for file upload and text input
uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type="pdf", help="Please upload your resume in PDF format.")
st.subheader("Job Responsibilities")
st.write(job_responsibilities)
jd = st.text_area("Job Description", height=200, max_chars=None)
st.subheader("Job Requirements")
st.write(job_requirements)

# Function to handle submission
def handle_submit():
    if uploaded_file is None or jd == "":
        st.error("Please upload a resume PDF and provide a job description.")
        return
    
    try:
        # Convert resume PDF to base64
        resume_base64 = convert_file_to_base64(uploaded_file)

        # Prepare data for sending to Cloud Function
        data = {
            'jd': jd,
            'resume_pdf': resume_base64
        }

        # Send POST request to Cloud Function
        cloud_function_url = 'https://us-central1-optical-torch-427812-i5.cloudfunctions.net/resume-matcher-function'  # Replace with your actual Cloud Function URL
        response = requests.post(cloud_function_url, json=data)

        # Process response
        if response.status_code == 200:
            result = response.json().get('result')
            st.subheader("Evaluation Result:")
            st.json(result)
        else:
            st.error(f"Error: {response.status_code} - {response.text}")

    except Exception as e:
        st.error(f"Error processing your request: {str(e)}")

# Streamlit button to submit the form
if st.button("Evaluate"):
    handle_submit()

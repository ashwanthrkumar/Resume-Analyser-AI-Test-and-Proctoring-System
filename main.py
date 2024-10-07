import streamlit as st
import subprocess

# Function to execute resume.py using subprocess
def execute_resume_py():
    subprocess.run(['python', 'resume.py'])

# Streamlit app logic
def main():
    st.title('Resume Matcher ATS')
    st.header('Click below to execute resume.py')

    if st.button('Execute resume.py'):
        st.write('Executing resume.py...')
        execute_resume_py()
        st.write('resume.py execution completed.')

if __name__ == '__main__':
    main()

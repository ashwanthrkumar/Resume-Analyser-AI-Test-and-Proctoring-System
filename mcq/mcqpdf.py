from flask import Flask, render_template, request, redirect, url_for
import google.generativeai as genai
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)

def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

# Function to configure Gemini AI model with the provided API key
def configure_gemini_api(api_key):
    genai.configure(api_key=api_key)

# Replace with your actual API key
API_KEY = 'AIzaSyDTenTn5lavhor_cot1odUWBJmScuR6G30'
configure_gemini_api(API_KEY)

# Function to generate MCQs and save to a PDF document
def generate_mcqs():
    mcq_list = []

    input_prompt = """
    Generate 25 different frequently asked technical questions in an interview. the response shud have a question, 
    4 options and one correct answer, shuffle the correct answer in unique way

    Demo Response:
    Question (number): %
    Option A: %
    Option B: %
    Option C: %
    Option D: %
    Correct Answer: %
    """

    options = get_gemini_response(input_prompt)
    if options:
        mcq_list.append({
            "options": options
        })

    output_path = "generated_mcqs.pdf"
    save_mcq_to_pdf(mcq_list, output_path)

    return mcq_list, output_path

# Function to save MCQs to a PDF document
def save_mcq_to_pdf(mcq_list, output_path):
    c = canvas.Canvas(output_path, pagesize=letter)
    y_position = 750  # Starting y position

    for mcq in mcq_list:
        options = mcq['options'].split("\n")
        for option in options:
            c.drawString(100, y_position, option)
            y_position -= 15  # Move to the next line

        c.drawString(100, y_position, "")  # Empty line for separation
        y_position -= 30  # Additional space between questions

    c.save()

    return output_path

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Generate MCQs and save to document
@app.route('/generate_mcqs', methods=['POST'])
def generate_mcqs_route():
    mcq_list, output_path = generate_mcqs()
    return redirect(url_for('show_mcqs'))

# Show generated MCQs
@app.route('/show_mcqs')
def show_mcqs():
    return render_template('show_mcqs.html', output_path="generated_mcqs.pdf")

# Evaluate MCQ answers and display results (if needed)
# This part depends on your application's requirements
# If you need to evaluate answers, you can implement it here.

if __name__ == '__main__':
    app.run(debug=True)

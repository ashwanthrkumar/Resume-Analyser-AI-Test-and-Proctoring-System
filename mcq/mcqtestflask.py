from flask import Flask, render_template, request, redirect, url_for, make_response
import re
from docx import Document

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Global variables to store questions, options, and correct answers
questions = []
options = []
correct_answers = []

def read_docx(file_path):
    # Load the document
    doc = Document(file_path)

    # Initialize a list to hold all the paragraphs
    paragraphs = []

    # Iterate through each paragraph in the document
    for paragraph in doc.paragraphs:
        paragraphs.append(paragraph.text)

    return "\n".join(paragraphs)

def parsing():
    global questions, options, correct_answers
    file_path = 'generated_mcqs.docx'
    text = read_docx(file_path)

    questions = []
    options = []
    correct_answers = []

    # Define the first regex pattern
    pattern1 = re.compile(
        r'\*\*Question \d+:\*\*\n(.*?)\nOption A:\s(.*?)\nOption B:\s(.*?)\nOption C:\s(.*?)\nOption D:\s(.*?)\nCorrect Answer:\s(.*?)\n',
        re.DOTALL
    )

    # Define the alternative regex pattern
    pattern2 = re.compile(
        r'\d+\.\sQuestion:\s(.*?)\n\s*Option A:\s(.*?)\n\s*Option B:\s(.*?)\n\s*Option C:\s(.*?)\n\s*Option D:\s(.*?)\n\s*Correct Answer:\s(.*?)\n',
        re.DOTALL
    )

    # Find all matches using the first pattern
    matches = pattern1.findall(text)

    # If the first pattern doesn't match any, use the alternative pattern
    if not matches:
        matches = pattern2.findall(text)

    # Extract and store questions, options, and correct answers
    for match in matches:
        question = match[0].strip()
        option_list = [match[1].strip(), match[2].strip(), match[3].strip(), match[4].strip()]
        correct_answer = match[5].strip()

        questions.append(question)
        options.append(option_list)
        correct_answers.append(correct_answer)

    # Map correct answers to their corresponding index
    correct_answers = [ord(answer) - ord('A') for answer in correct_answers]

    # Debugging: Print the number of questions parsed
    print(f"Total questions parsed: {len(questions)}")

    # Print details for further debugging
    print("Questions, options, and correct answers:")
    for i, question in enumerate(questions):
        print(f"Q{i+1}: {question}")
        for j, option in enumerate(options[i]):
            print(f"Option {chr(65+j)}: {option}")
        print(f"Correct Answer: {chr(65+correct_answers[i])}\n")

# Parse the questions, options, and correct answers once at startup
parsing()

@app.route('/', methods=['GET', 'POST'])
def index():
    question_index = int(request.args.get('q', 0))

    # Debugging: Print the current question index and total questions
    print(f"Current question index: {question_index}")
    print(f"Total questions: {len(questions)}")

    if question_index >= len(questions):
        # If all questions are answered, redirect to the finish page
        return redirect(url_for('finish'))

    if request.method == 'POST':
        # Handle form submission
        user_answer = int(request.form['option'])

        # Store user answer in cookies for comparison in 'finish' route
        response = make_response(redirect(url_for('index', q=question_index + 1)))
        response.set_cookie(f'q-{question_index}', str(user_answer))
        return response

    return render_template('index.html', question_index=question_index, question=questions[question_index], options=options[question_index])

@app.route('/finish')
def finish():
    total_questions = len(questions)
    total_correct = sum(1 for i in range(len(questions)) if int(request.cookies.get(f'q-{i}')) == correct_answers[i])
    return render_template('finish.html', total_questions=total_questions, total_correct=total_correct)

if __name__ == '__main__':
    app.run(debug=True)

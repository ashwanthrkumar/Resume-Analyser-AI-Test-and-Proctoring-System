from flask import Flask, render_template, request, redirect, url_for, session
from docx import Document
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'


# Parse the docx file
def parse_docx(file_path):
    document = Document(file_path)
    questions = []
    current_question = {'question': '', 'options': [], 'correct_answer': ''}

    for para in document.paragraphs:
        text = para.text.strip()
        if re.match(r'^\d+\.', text):
            if current_question['question']:
                questions.append(current_question)
            current_question = {'question': text, 'options': [], 'correct_answer': ''}
        elif re.match(r'^[ABCD]:', text):
            current_question['options'].append(text)
        elif text.startswith('Correct Answer:'):
            current_question['correct_answer'] = text.split(':')[1].strip()

    if current_question['question']:
        questions.append(current_question)

    return questions


questions = parse_docx('generated_mcqs.docx')


@app.route('/', methods=['GET', 'POST'])
def quiz():
    if 'current_question' not in session:
        session['current_question'] = 0
        session['user_answers'] = []

    if request.method == 'POST':
        user_answer = request.form.get('answer')
        session['user_answers'].append(user_answer)

        session['current_question'] += 1
        if session['current_question'] >= len(questions):
            return redirect(url_for('result'))

    current_question = questions[session['current_question']]
    return render_template('quiz.html', question=current_question, q_num=session['current_question'] + 1)


@app.route('/result')
def result():
    user_answers = session.get('user_answers', [])
    correct_count = 0
    for i, question in enumerate(questions):
        if i < len(user_answers) and user_answers[i] == question['correct_answer']:
            correct_count += 1
    return render_template('results.html', correct_count=correct_count, total=len(questions))


if __name__ == '__main__':
    app.run(debug=True)

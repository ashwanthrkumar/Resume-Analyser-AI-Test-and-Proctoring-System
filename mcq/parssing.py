import re
from docx import Document

def read_docx(file_path):
    # Load the document
    doc = Document(file_path)

    # Initialize a list to hold all the paragraphs
    paragraphs = []

    # Iterate through each paragraph in the document
    for paragraph in doc.paragraphs:
        paragraphs.append(paragraph.text)

    return "\n".join(paragraphs)

file_path = 'generated_mcqs.docx'
text = read_docx(file_path)

questions = []
options = []
correct_answers = []

# Define the first regex pattern
pattern1 = re.compile(
    r'\*\*Question \d:\*\*\n(.*?)\nOption A:\s(.*?)\nOption B:\s(.*?)\nOption C:\s(.*?)\nOption D:\s(.*?)\nCorrect Answer:\s(.*?)\n',
    re.DOTALL
)

# Define the alternative regex pattern
pattern2 = re.compile(
    r'\d+\.\sQuestion:\s(.*?)\n\s+Option A:\s(.*?)\n\s+Option B:\s(.*?)\n\s+Option C:\s(.*?)\n\s+Option D:\s(.*?)\n\s+Correct Answer:\s(.*?)\n',
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

# Print the results
print("Questions:")
for q in questions:
    print(q)

print("\nOptions:")
for option_list in options:
    for i, o in enumerate(option_list, start=1):
        print(f"Option {chr(64+i)}: {o}")
    print()

print("\nCorrect Answers:")
for ca in correct_answers:
    print(ca)

print(options[3])
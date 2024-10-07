from docx import Document

def parse_practice_questions(document_path):
  """Parses a docx document containing practice questions and stores them in a list.

  Args:
      document_path: The path to the docx document.

  Returns:
      A list of dictionaries, where each dictionary represents a practice question
      with keys 'question', 'options', and 'answer'.
  """
  document = Document(document_path)
  questions = []

  for paragraph in document.paragraphs:
    text = paragraph.text.strip()
    question = ""
    options = []
    if text.isdigit():  # Check if line starts with a number
      question_number = int(text)
      question = ""
      options = []
    elif text.startswith("A:"):  # Check if line starts with option A
      options.append(text.strip("A:"))
    elif text.startswith("B:"):
      options.append(text.strip("B:"))
    elif text.startswith("C:"):
      options.append(text.strip("C:"))
    elif text.startswith("D:"):
      options.append(text.strip("D:"))
    elif text.startswith("Correct Answer:"):  # Check for answer line
      answer = text.strip("Correct Answer:")
      questions.append({
          "question": question,
          "options": options,
          "answer": answer
      })
    else:  # Append non-formatted text to the question string
      question += text + "\n"

  return questions

if __name__ == "__main__":
  document_path = "generated_mcqs.docx"  # Replace with your file path
  questions = parse_practice_questions(document_path)

  for question in questions:
    print(f"Question {question['question']}")
    for i, option in enumerate(question['options']):
      print(f"  Option {chr(i+65)}: {option}")  # Print options with A, B, C, D labels
    print(f"  Correct Answer: {question['answer']}")
    print()  # Print blank line between questions

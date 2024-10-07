import tkinter as tk
from tkinter import messagebox

class MCQTestApp:
    def __init__(self, questions, options, correct_answers):
        self.questions = questions
        self.options = options
        self.correct_answers = correct_answers
        self.selected_answers = [None] * len(questions)  # Initialize selected answers list

        self.current_question_index = 0  # Track the current question index

        self.root = tk.Tk()
        self.root.title("MCQ Test")

        self.question_label = tk.Label(self.root, text="", wraplength=600, justify="left", padx=10, pady=10)
        self.question_label.pack()

        self.option_var = tk.StringVar()
        self.option_buttons = []

        for i in range(len(options[0])):
            option_button = tk.Radiobutton(self.root, text="", variable=self.option_var, value=i, padx=10, pady=5)
            option_button.pack(anchor="w")
            self.option_buttons.append(option_button)

        self.next_button = tk.Button(self.root, text="Next", command=self.next_question)
        self.next_button.pack(pady=10)

        self.finish_button = tk.Button(self.root, text="Finish", command=self.finish_test)

        self.load_question(self.current_question_index)

    def load_question(self, index):
        self.question_label.config(text=f"{self.questions[index]}")

        for i in range(len(self.options[index])):
            self.option_buttons[i].config(text=f"{chr(65 + i)}. {self.options[index][i]}")

        # If an answer is already selected, update the radio button selection
        if self.selected_answers[index] is not None:
            self.option_var.set(self.selected_answers[index])
        else:
            self.option_var.set(None)

        # Show/hide finish button based on whether it's the last question
        if index == len(self.questions) - 1:
            self.next_button.pack_forget()
            self.finish_button.pack(pady=10)
        else:
            self.next_button.pack(pady=10)
            self.finish_button.pack_forget()

    def next_question(self):
        selected_index = self.option_var.get()
        if selected_index is not None:
            self.selected_answers[self.current_question_index] = selected_index
            self.current_question_index += 1
            if self.current_question_index < len(self.questions):
                self.load_question(self.current_question_index)
        else:
            messagebox.showwarning("Warning", "Please select an option before proceeding.")

    def finish_test(self):
        selected_answers = self.selected_answers
        correct_answers = self.correct_answers

        # Evaluate answers
        score = 0
        for i in range(len(correct_answers)):
            if selected_answers[i] is not None and int(selected_answers[i]) == correct_answers[i]:
                score += 1

        # Display evaluation
        messagebox.showinfo("Test Result", f"You scored {score} out of {len(correct_answers)}.")

        # Close the application
        self.root.destroy()

    def run(self):
        self.root.mainloop()

# Example usage
questions = [
    "Which of the following is a low-level programming language?",
    "What is the purpose of a database?",
    "Which data structure is used to implement a queue?",
    "What is the difference between a class and an object in OOP?",
    "What is the purpose of an exception handling mechanism?"
]

options = [
    ["Python", "C++", "Assembly", "JavaScript"],
    ["To store and manage data", "To process data", "To display data", "To analyze data"],
    ["Stack", "Array", "Queue", "Linked list"],
    ["A class is a blueprint, and an object is an instance of the class",
     "An object is a blueprint, and a class is an instance of the object",
     "Both are the same",
     "There is no difference"],
    ["To handle errors and prevent program crashes", "To improve code readability",
     "To enhance performance", "To simplify debugging"]
]

correct_answers = [2, 0, 2, 0, 0]  # Index of correct options for each question

# Create and run the MCQ test application
app = MCQTestApp(questions, options, correct_answers)
app.run()

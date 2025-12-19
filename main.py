import tkinter as tk
from ui import QuizUI
from core import load_questions, check_answer
from extra_features import randomize_questions, filter_by_difficulty


class QuizController:
    def __init__(self, root) :
        self.ui = QuizUI(root)

        # Bind GUI callbacks
        self.ui.bind_start(self.start_quiz)
        self.ui.bind_retry(self.retry_quiz)
        self.ui.bind_answer(self.answer_selected)

        # Internal state
        self.questions = []
        self.current_index = 0
        self.score = 0

    def start_quiz(self):
        all_questions = load_questions()
        level = self.ui.diff_var.get()

        # Apply extra features
        filtered = filter_by_difficulty(all_questions, level)
        self.questions = randomize_questions(filtered)

        if not self.questions:
            self.ui.question_text.set("No questions for this difficulty.")
            return

        # Reset score & index
        self.score = 0
        self.current_index = 0
        self.ui.update_score(self.score, len(self.questions))

        # Show first question
        self.show_question()
        def show_question(self):
        q = self.questions[self.current_index]
        self.ui.display_question(q)

    def answer_selected(self, answer):
        if not self.questions:
            return

        q = self.questions[self.current_index]

        # Check answer
        if check_answer(answer, q["answer"]):
            self.score += 1

        self.current_index += 1
        self.ui.update_score(self.score, len(self.questions))

        if self.current_index >= len(self.questions):
            self.ui.question_text.set("Quiz completed! Check your score above.")
        else:
            self.show_question()

    def retry_quiz(self):
        # Reset and start quiz again
        self.start_quiz()


if __name__ == "__main__":
    root = tk.Tk()
    controller = QuizController(root)
    root.mainloop()

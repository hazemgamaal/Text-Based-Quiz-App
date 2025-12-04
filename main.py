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
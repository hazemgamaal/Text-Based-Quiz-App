import tkinter as tk
from tkinter import messagebox
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
        self.timer_id = None
        self.time_per_question = 15

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
        # reset UI state for new question
        total = len(self.questions)
        self.ui.set_progress(self.current_index + 1, total)
        self.ui.reset_option_styles()
        self.ui.enable_options()
        self.ui.display_question(q)

        # start timer
        self.start_timer(self.time_per_question)

    def start_timer(self, seconds):
        # cancel existing timer if any
        if self.timer_id:
            self.ui.root.after_cancel(self.timer_id)
            self.timer_id = None

        def tick(remaining):
            self.ui.set_timer(f"Time: {remaining}s")
            if remaining <= 0:
                # time up -> treat as no answer
                self.process_answer(None)
                return
            self.timer_id = self.ui.root.after(1000, lambda: tick(remaining - 1))

        tick(seconds)

    def answer_selected(self, answer):
        # guard
        if not self.questions:
            return
        # disable further input immediately
        self.ui.disable_options()
        # handle answer processing
        self.process_answer(answer)

    def process_answer(self, selected_key):
        # stop timer
        if self.timer_id:
            try:
                self.ui.root.after_cancel(self.timer_id)
            except Exception:
                pass
            self.timer_id = None

        q = self.questions[self.current_index]
        correct = q["answer"]

        # score update
        if selected_key and check_answer(selected_key, correct):
            self.score += 1

        # highlight choices
        self.ui.highlight_options(correct_key=correct, selected_key=selected_key)

        # update score display
        self.ui.update_score(self.score, len(self.questions))

        # move to next question after short delay
        def next_q():
            self.current_index += 1
            if self.current_index >= len(self.questions):
                # finished
                self.finish_quiz()
            else:
                self.show_question()

        # schedule next
        self.ui.root.after(1000, next_q)

    def finish_quiz(self):
        self.ui.set_timer("")
        self.ui.set_progress(len(self.questions), len(self.questions))
        msg = f"You scored {self.score} out of {len(self.questions)}."
        if messagebox.askyesno("Quiz Completed", msg + "\n\nPlay again?"):
            self.retry_quiz()
        else:
            self.ui.question_text.set("Quiz completed! Thank you for playing.")

    def retry_quiz(self):
        # Reset and start quiz again
        self.start_quiz()


if __name__ == "__main__":
    root = tk.Tk()
    controller = QuizController(root)
    root.mainloop()



import tkinter as tk
from tkinter import messagebox

class QuizUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Application")
        self.root.geometry("650x450")
        self.root.configure(bg="#f0f0f0")

        self.question_text = tk.StringVar()
        self.score_label_text = tk.StringVar()

        # Title
        tk.Label(root, text="Quiz Application", font=("Arial", 22, "bold"), bg="#f0f0f0").pack(pady=10)

        # Difficulty Frame
        self.diff_frame = tk.Frame(root, bg="#f0f0f0")
        self.diff_frame.pack()

        tk.Label(self.diff_frame, text="Choose Difficulty:", bg="#f0f0f0", font=("Arial", 12)).grid(row=0, column=0, padx=5)

        self.diff_var = tk.StringVar(value="all")
        tk.OptionMenu(self.diff_frame, self.diff_var, "easy", "medium", "hard", "all").grid(row=0, column=1)

        # Start Button
        self.start_btn = tk.Button(root, text="Start Quiz", font=("Arial", 12), command=None)
        self.start_btn.pack(pady=10)

        # Question Label
        self.question_label = tk.Label(root, textvariable=self.question_text, wraplength=550, font=("Arial", 14), bg="#f0f0f0")
        self.question_label.pack(pady=10)

        # Option Buttons
        self.buttons = {}
        options = ["A", "B", "C", "D"]

        for opt in options:
            btn = tk.Button(root, text=f"{opt}: ", width=40, font=("Arial", 12),
                            command=lambda o=opt: self.select_answer(o))
            btn.pack(pady=3)
            self.buttons[opt] = btn

        # Score Label
        tk.Label(root, textvariable=self.score_label_text, font=("Arial", 12), bg="#f0f0f0").pack(pady=5)

        # Retry Button
        self.retry_btn = tk.Button(root, text="Retry Quiz", font=("Arial", 12), command=None)
        self.retry_btn.pack(pady=10)

        # Function placeholders (connected by main.py)
        self.on_start = None
        self.on_answer = None
        self.on_retry = None

    def bind_start(self, callback):
        self.on_start = callback
        self.start_btn.config(command=callback)

    def bind_answer(self, callback):
        self.on_answer = callback

    def bind_retry(self, callback):
        self.on_retry = callback
        self.retry_btn.config(command=callback)

    def display_question(self, q):
        self.question_text.set(q["question"])
        for key, btn in self.buttons.items():
            btn.config(text=f"{key}: {q['options'][key]}")

    def select_answer(self, option):
        if self.on_answer:
            self.on_answer(option)

    def update_score(self, score, total):
        self.score_label_text.set(f"Score: {score}/{total}")

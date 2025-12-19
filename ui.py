import tkinter as tk
from tkinter import messagebox


class QuizUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Application")
        self.root.geometry("650x450")
        # overall app background (dark)
        self.root.configure(bg="#1e293b")

        self.question_text = tk.StringVar()
        self.score_label_text = tk.StringVar()
        self.progress_text = tk.StringVar()
        self.timer_text = tk.StringVar()

        # Title (teal banner)
        tk.Label(root, text="Quiz Application", font=("Arial", 22, "bold"), bg="#0ea5a4", fg="#ffffff", padx=10, pady=8).pack(pady=10, fill="x")

        # Difficulty Frame
        self.diff_frame = tk.Frame(root, bg="#1e293b")
        self.diff_frame.pack()

        tk.Label(self.diff_frame, text="Choose Difficulty:", bg="#1e293b", fg="#ffffff", font=("Arial", 12)).grid(row=0, column=0, padx=5)

        self.diff_var = tk.StringVar(value="all")
        tk.OptionMenu(self.diff_frame, self.diff_var, "easy", "medium", "hard", "all").grid(row=0, column=1)

        # Control row with Start and Start From Beginning buttons
        controls = tk.Frame(root, bg="#1e293b")
        controls.pack(pady=10)

        # Start Button (left)
        self.start_btn = tk.Button(controls, text="Start Quiz", font=("Arial", 12), command=None,
                       bg="#0ea5a4", fg="#ffffff", activebackground="#057f77", width=16, padx=6, pady=4)
        self.start_btn.pack(side="left", padx=6)

        # Progress & Timer
        info_frame = tk.Frame(root, bg="#1e293b")
        info_frame.pack()
        tk.Label(info_frame, textvariable=self.progress_text, font=("Arial", 11), bg="#1e293b", fg="#ffffff").grid(row=0, column=0, padx=10)
        tk.Label(info_frame, textvariable=self.timer_text, font=("Arial", 11), bg="#1e293b", fg="#ffffff").grid(row=0, column=1, padx=10)

        # Question Label (card)
        self.question_label = tk.Label(root, textvariable=self.question_text, wraplength=550, font=("Arial", 14), bg="#f8fafc", fg="#0b1220", bd=2, relief="groove")
        self.question_label.pack(pady=10, padx=12, fill="x")

        # Option Buttons
        self.buttons = {}
        options = ["A", "B", "C", "D"]

        for opt in options:
            btn = tk.Button(root, text=f"{opt}: ", width=40, font=("Arial", 12),
                            command=lambda o=opt: self.select_answer(o),
                            bg="#e6eef3", fg="#0b1220", activebackground="#cfe7f5")
            btn.pack(pady=3)
            self.buttons[opt] = btn

        # remember default button background for reset
        self.default_btn_bg = "#e6eef3"

        # Score Label
        tk.Label(root, textvariable=self.score_label_text, font=("Arial", 12), bg="#1e293b", fg="#ffffff").pack(pady=5)

        # Retry / Start From Beginning Button (right, smaller)
        self.retry_btn = tk.Button(controls, text="Start From Beginning", font=("Arial", 11), command=None,
                       bg="#0ea5a4", fg="#ffffff", activebackground="#057f77", width=18, padx=6, pady=4)
        self.retry_btn.pack(side="left", padx=6)

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

    def set_progress(self, current, total):
        self.progress_text.set(f"Question: {current}/{total}")

    def set_timer(self, text):
        self.timer_text.set(text)

    def disable_options(self):
        for b in self.buttons.values():
            b.config(state="disabled")

    def enable_options(self):
        for b in self.buttons.values():
            b.config(state="normal")

    def highlight_options(self, correct_key, selected_key=None):
        # color correct green, selected wrong red, others reset
        for key, btn in self.buttons.items():
            if key == correct_key:
                btn.config(bg="#c8e6c9")
            elif selected_key and key == selected_key:
                btn.config(bg="#ffcdd2")
            else:
                btn.config(bg=self.default_btn_bg)

    def reset_option_styles(self):
        for btn in self.buttons.values():
            btn.config(bg=self.default_btn_bg, state="normal")

    def display_question(self, q):
        self.question_text.set(q["question"])
        for key, btn in self.buttons.items():
            # guard if option missing
            text = q.get('options', {}).get(key, '')
            btn.config(text=f"{key}: {text}")

    def select_answer(self, option):
        if self.on_answer:
            self.on_answer(option)

    def update_score(self, score, total):
        self.score_label_text.set(f"Score: {score}/{total}")


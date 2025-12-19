import json
import importlib

import pytest



class DummyVar:
    def __init__(self, value="all"):
        self._v = value

    def get(self):
        return self._v


class MockUI:
    def __init__(self, root=None):
        self.root = root or self
        # simple var-like object
        self.diff_var = DummyVar("all")
        # emulate a StringVar-like for question_text
        class _Q:
            def __init__(self):
                self._last = None

            def set(self, v):
                self._last = v

        self.question_text = _Q()
        self.displayed = []
        self.score_updates = []
        self.progress = []
        self.timer = []
        # scheduled callbacks (ms, cb)
        self._scheduled = []

    def bind_start(self, cb):
        self._start_cb = cb

    def bind_answer(self, cb):
        self._answer_cb = cb

    def bind_retry(self, cb):
        self._retry_cb = cb

    def display_question(self, q):
        self.displayed.append(q)

    def update_score(self, score, total):
        self.score_updates.append((score, total))

    def set_progress(self, cur, tot):
        self.progress.append((cur, tot))

    def set_timer(self, text):
        self.timer.append(text)

    def enable_options(self):
        pass

    def disable_options(self):
        pass

    def highlight_options(self, correct_key, selected_key=None):
        pass

    def reset_option_styles(self):
        pass

    # minimal 'after' handlers used by controller.timer logic: collect callbacks
    def after(self, ms, cb):
        # store callbacks; tests can run them via `run_scheduled()`
        self._scheduled.append((ms, cb))
        return len(self._scheduled) - 1

    def after_cancel(self, id):
        try:
            self._scheduled[id] = (None, lambda: None)
        except Exception:
            pass

    def run_scheduled(self):
        # Run and clear all scheduled callbacks in order
        callbacks = self._scheduled[:]
        self._scheduled.clear()
        for ms, cb in callbacks:
            try:
                cb()
            except Exception:
                raise


def test_quiz_controller_flow(monkeypatch, tmp_path):
    # prepare questions.json
    questions = [
        {"question": "Q1", "options": {"A": "a", "B": "b"}, "answer": "A", "difficulty": "all"},
        {"question": "Q2", "options": {"A": "x", "B": "y"}, "answer": "B", "difficulty": "all"},
    ]
    p = tmp_path / "questions.json"
    p.write_text(json.dumps(questions))

    # monkeypatch cwd so core.load_questions finds file
    monkeypatch.chdir(tmp_path)

    # monkeypatch ui.QuizUI before importing main
    import ui

    monkeypatch.setattr(ui, "QuizUI", MockUI)

    # reload main to pick up patched UI
    import main
    importlib.reload(main)

    # create controller with Mock root
    controller = main.QuizController(root=None)
    # avoid timer auto-expiry during tests
    controller.time_per_question = 1000

    # start quiz
    controller.start_quiz()
    assert len(controller.questions) == 2
    # first question displayed (order may be randomized)
    assert controller.ui.displayed, "No question displayed"

    first_q = controller.ui.displayed[0]
    # answer first correctly using its answer key
    controller.answer_selected(first_q["answer"])
    # run pending scheduled callbacks (advance to next question)
    controller.ui.run_scheduled()
    assert controller.score == 1

    # answer second incorrectly (choose an option key that's not the correct one)
    second_q = controller.ui.displayed[1]
    wrong_key = next((k for k in second_q["options"].keys() if k != second_q["answer"]), None)
    controller.answer_selected(wrong_key)
    # do not run scheduled callbacks (which would finish the quiz); score should remain
    assert controller.score == 1


def test_empty_filtered_questions_shows_message(monkeypatch, tmp_path):
    questions = [
        {"question": "QX", "options": {"A": "a"}, "answer": "A", "difficulty": "hard"}
    ]
    p = tmp_path / "questions.json"
    p.write_text(json.dumps(questions))
    monkeypatch.chdir(tmp_path)

    import ui
    monkeypatch.setattr(ui, "QuizUI", MockUI)
    import importlib, main
    importlib.reload(main)

    controller = main.QuizController(root=None)
    # set UI difficulty to 'easy' which filters out the only hard question
    controller.ui.diff_var = DummyVar("easy")
    controller.start_quiz()
    # MockUI.question_text should contain the message
    assert "No questions" in controller.ui.question_text._last


def test_retry_resets_state(monkeypatch, tmp_path):
    questions = [
        {"question": "Q1", "options": {"A": "a"}, "answer": "A", "difficulty": "all"},
        {"question": "Q2", "options": {"A": "b"}, "answer": "A", "difficulty": "all"},
    ]
    p = tmp_path / "questions.json"
    p.write_text(json.dumps(questions))
    monkeypatch.chdir(tmp_path)

    import ui
    monkeypatch.setattr(ui, "QuizUI", MockUI)
    import importlib, main
    importlib.reload(main)

    controller = main.QuizController(root=None)
    controller.time_per_question = 1000
    controller.start_quiz()
    controller.answer_selected("A")
    # advance scheduled next question
    controller.ui.run_scheduled()
    assert controller.score == 1
    # call retry
    controller.retry_quiz()
    assert controller.score == 0
    assert controller.current_index == 0

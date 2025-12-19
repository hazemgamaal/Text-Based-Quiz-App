import json
from pathlib import Path

import pytest

import core


def test_load_questions_and_check_answer(tmp_path, monkeypatch):
    data = [
        {"question": "Q1", "options": {"A": "a", "B": "b"}, "answer": "A", "difficulty": "easy"},
        {"question": "Q2", "options": {"A": "x", "B": "y"}, "answer": "B", "difficulty": "hard"},
    ]

    p = tmp_path / "questions.json"
    p.write_text(json.dumps(data))

    # run load_questions in tmp dir
    monkeypatch.chdir(tmp_path)
    loaded = core.load_questions()
    assert isinstance(loaded, list)
    assert loaded == data

    # check_answer
    assert core.check_answer("A", "A") is True
    assert core.check_answer("B", "A") is False


def test_load_questions_file_missing(tmp_path, monkeypatch):
    # ensure FileNotFoundError is raised when file missing
    monkeypatch.chdir(tmp_path)
    import pytest

    with pytest.raises(FileNotFoundError):
        core.load_questions()

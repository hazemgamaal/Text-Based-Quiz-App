import copy

from extra_features import randomize_questions, filter_by_difficulty


def test_filter_by_difficulty():
    questions = [
        {"question": "Q1", "difficulty": "easy"},
        {"question": "Q2", "difficulty": "medium"},
        {"question": "Q3", "difficulty": "hard"},
    ]

    assert filter_by_difficulty(questions, "easy") == [questions[0]]
    assert filter_by_difficulty(questions, "all") == questions


def test_randomize_questions_preserves_items():
    questions = [
        {"id": i} for i in range(10)
    ]
    original = copy.deepcopy(questions)
    shuffled = randomize_questions(questions[:])
    # same elements (by id)
    assert {q["id"] for q in shuffled} == {q["id"] for q in original}


def test_filter_unknown_level_returns_empty():
    questions = [{"question": "Q1", "difficulty": "easy"}]
    assert filter_by_difficulty(questions, "unknown") == []


def test_randomize_questions_calls_shuffle(monkeypatch):
    called = {"called": False}

    def fake_shuffle(lst):
        called["called"] = True
        lst.reverse()

    monkeypatch.setattr("random.shuffle", fake_shuffle)

    q = [{"id": 1}, {"id": 2}, {"id": 3}]
    out = randomize_questions(q)
    assert called["called"] is True
    assert [x["id"] for x in out] == [3, 2, 1]

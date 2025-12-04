import random

def randomize_questions(questions):
    random.shuffle(questions)
    return questions

def filter_by_difficulty(questions, level):
    if level == "all":
        return questions
    return [q for q in questions if q["difficulty"] == level]

def ask_retry_gui():
    """This is handled by GUI, but function kept for project completeness."""
    pass

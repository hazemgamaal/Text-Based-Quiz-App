import json

def load_questions():
    """Load questions from a JSON file."""
    with open("questions.json", "r") as file:
        return json.load(file)

def check_answer(user_answer, correct_answer):
    """Return True/False depending on match."""
    return user_answer == correct_answer

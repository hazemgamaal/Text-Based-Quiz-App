import streamlit as st
import time
from core import load_questions, check_answer
from extra_features import randomize_questions, filter_by_difficulty

# Initialize session state
if "questions" not in st.session_state:
    st.session_state.questions = []
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
if "quiz_finished" not in st.session_state:
    st.session_state.quiz_finished = False
if "question_start_time" not in st.session_state:
    st.session_state.question_start_time = None
if "time_per_question" not in st.session_state:
    st.session_state.time_per_question = 15
if "selected_answer" not in st.session_state:
    st.session_state.selected_answer = None
if "show_result" not in st.session_state:
    st.session_state.show_result = False
if "correct_answer" not in st.session_state:
    st.session_state.correct_answer = None

st.title("Quiz Application")

# Difficulty selection
difficulty = st.selectbox(
    "Choose Difficulty:", ["easy", "medium", "hard", "all"], index=3
)

# Control buttons
col1, col2 = st.columns(2)
with col1:
    start_quiz = st.button("Start Quiz", use_container_width=True)
with col2:
    retry_quiz = st.button("Start From Beginning", use_container_width=True)

# Start quiz
if start_quiz or retry_quiz:
    all_questions = load_questions()
    filtered = filter_by_difficulty(all_questions, difficulty)
    st.session_state.questions = randomize_questions(filtered)

    if not st.session_state.questions:
        st.warning("No questions available for this difficulty level.")
        st.session_state.quiz_started = False
    else:
        st.session_state.quiz_started = True
        st.session_state.quiz_finished = False
        st.session_state.current_index = 0
        st.session_state.score = 0
        st.session_state.selected_answer = None
        st.session_state.show_result = False
        st.session_state.question_start_time = time.time()
        st.rerun()

# Quiz finished check (must be before the main quiz logic)
if st.session_state.quiz_started and st.session_state.quiz_finished:
    total = len(st.session_state.questions)
    st.balloons()
    st.success(
        f"🎉 Quiz Completed! You scored {st.session_state.score} out of {total}."
    )

    if st.button("Play Again"):
        st.session_state.quiz_started = False
        st.session_state.quiz_finished = False
        st.rerun()

# Quiz logic
elif st.session_state.quiz_started and not st.session_state.quiz_finished:
    if st.session_state.current_index < len(st.session_state.questions):
        q = st.session_state.questions[st.session_state.current_index]
        total = len(st.session_state.questions)

        # Progress and timer
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Question: {st.session_state.current_index + 1}/{total}**")
        with col2:
            if (
                st.session_state.question_start_time
                and not st.session_state.show_result
            ):
                elapsed = time.time() - st.session_state.question_start_time
                remaining = max(0, int(st.session_state.time_per_question - elapsed))
                st.write(f"**Time: {remaining}s**")

                # Auto-advance if time runs out
                if remaining <= 0 and not st.session_state.show_result:
                    st.session_state.selected_answer = None
                    st.session_state.show_result = True
                    st.session_state.correct_answer = q["answer"]
                    if check_answer(None, q["answer"]):
                        st.session_state.score += 1
                    st.rerun()
            else:
                st.write("**Time: 0s**")

        # Progress bar
        progress = (st.session_state.current_index + 1) / total
        st.progress(progress)

        # Display question
        st.markdown(f"### {q['question']}")

        # Answer options
        if not st.session_state.show_result:
            options = []
            option_keys = ["A", "B", "C", "D"]
            for key in option_keys:
                if key in q.get("options", {}):
                    options.append(f"{key}: {q['options'][key]}")

            selected = st.radio(
                "Select your answer:",
                options,
                key=f"question_{st.session_state.current_index}",
            )

            if st.button("Submit Answer"):
                selected_key = selected.split(":")[0] if selected else None
                st.session_state.selected_answer = selected_key
                st.session_state.correct_answer = q["answer"]
                st.session_state.show_result = True
                st.session_state.question_start_time = None

                # Check answer
                if check_answer(selected_key, q["answer"]):
                    st.session_state.score += 1

                st.rerun()
        else:
            # Show result
            st.session_state.correct_answer = q["answer"]
            option_keys = ["A", "B", "C", "D"]

            for key in option_keys:
                if key in q.get("options", {}):
                    option_text = f"{key}: {q['options'][key]}"
                    if key == st.session_state.correct_answer:
                        st.success(f"✓ {option_text} (Correct)")
                    elif key == st.session_state.selected_answer:
                        st.error(f"✗ {option_text} (Your answer)")
                    else:
                        st.write(option_text)

            # Score display
            st.write(f"**Score: {st.session_state.score}/{total}**")

            # Next question button
            if st.button("Next Question"):
                st.session_state.current_index += 1
                st.session_state.selected_answer = None
                st.session_state.show_result = False

                if st.session_state.current_index >= len(st.session_state.questions):
                    st.session_state.quiz_finished = True
                else:
                    st.session_state.question_start_time = time.time()
                st.rerun()
else:
    # Initial state - show welcome message
    st.info("Select a difficulty level and click 'Start Quiz' to begin!")

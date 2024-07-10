
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(user_id, answer):
    # Validate the answer (this can be customized based on your validation logic)
    if not answer:
        return "Answer cannot be empty."

    # Store the answer in the user's session or database
    user_session = get_user_session(user_id)
    current_question = user_session['current_question']
    user_session['answers'][current_question] = answer

    # Save the session
    save_user_session(user_id, user_session)

    return "Answer recorded."


def get_next_question(user_id):
    user_session = get_user_session(user_id)
    questions = user_session['questions']
    current_index = user_session.get('current_index', 0)

    if current_index < len(questions):
        next_question = questions[current_index]
        user_session['current_question'] = next_question
        user_session['current_index'] = current_index + 1
        save_user_session(user_id, user_session)
        return next_question
    else:
        return None  # No more questions left


def generate_final_response(user_id):
    user_session = get_user_session(user_id)
    answers = user_session['answers']
    correct_answers = 0

    # Assuming we have a dictionary of correct answers
    correct_answers_dict = {
        'question1': 'answer1',
        'question2': 'answer2',
        # Add all correct answers here
    }

    for question, answer in answers.items():
        if correct_answers_dict.get(question) == answer:
            correct_answers += 1

    total_questions = len(correct_answers_dict)
    score = (correct_answers / total_questions) * 100

    return f"Quiz completed! Your score is {score:.2f}%."

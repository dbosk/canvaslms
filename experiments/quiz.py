import canvasapi
import json
import os

canvas = canvasapi.Canvas(os.environ["CANVAS_SERVER"],
        os.environ["CANVAS_TOKEN"])

test_course = None

for course in canvas.get_courses():
    if course.name == "Sandbox dbosk":
        test_course = course
        break

test_quiz = None

for quiz in course.get_quizzes():
    if quiz.title == "Classic datorprov":
        test_quiz = quiz
        break

test_submission = None

# There is only one in my setup
for quiz_submission in test_quiz.get_submissions():
    test_submission = quiz_submission

print("\n# Quiz submission questions\n")

for subm_question in test_submission.get_submission_questions():
    #print(subm_question.__dict__.keys())
    #print(subm_question)
    print(f"{subm_question.id} "
          f"{subm_question.question_name}:\n"
          f"{subm_question.question_text}")
    try:
        print(f"Alternatives: {subm_question.answers}")
        print(f"Correct: {subm_question.correct}")
    except AttributeError:
        pass

    print()

print("\n# Quiz submission answers\n")

quiz = None

for assignment in test_course.get_assignments():
    if assignment.name == "Classic datorprov":
        quiz = assignment
        break

for submission in quiz.get_submissions(include=["submission_history"]):
    for subm in submission.submission_history:
        #print(subm)
        try:
            for data in subm["submission_data"]:
                print(json.dumps(data, indent=2))
        except KeyError:
            pass


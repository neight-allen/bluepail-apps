import logging
import os

from flask import Flask, jsonify, request

from brainstorm.main import Consultant

app = Flask(__name__, static_folder="static")

log_level = os.environ.get("LOG_LEVEL", "INFO")
logging.basicConfig(level=log_level)


@app.route("/api/v1/consultant/clarify", methods=["POST"])
def get_clarification():
    """
    This function expects a JSON data format with the following key:
    'problem-description': a string that describes the problem to be clarified.
    """
    data = request.get_json()
    problem_description = data["problem-description"]
    consultant = Consultant()
    clarification_questions = consultant.get_clarification(problem_description)
    return jsonify({"questions": clarification_questions})


@app.route("/api/v1/consultant/solve", methods=["POST"])
def get_solution():
    """
    This function expects a JSON data format with the following keys:
    'problem-description': a string that describes the problem to be solved.
    'clarification-answers': a list of strings that are the answers to the clarification questions.
    'number-of-solutions': an optional integer that specifies the number of solutions to return. Defaults to 3 if not provided.
    """
    data = request.get_json()
    problem_description = data["problem-description"]
    clarification_answers = data["clarification-answers"]
    number_of_solutions = data.get("number-of-solutions", 3)
    consultant = Consultant()
    solution = consultant.get_solution(
        problem_description, clarification_answers, number_of_solutions
    )
    return jsonify({"solution": solution})


if __name__ == "__main__":
    app.run(debug=True)

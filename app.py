import logging
import os

from flasgger import Swagger
from flask import Flask, jsonify, request

from brainstorm.main import Consultant

app = Flask(__name__, static_folder="static")
swagger = Swagger(app)

log_level = os.environ.get("LOG_LEVEL", "INFO")
logging.basicConfig(level=log_level)


@app.route("/api/v1/consultant/clarify", methods=["POST"])
def get_clarification():
    """
    This method accepts a POST request with a JSON object containing a problem description.
    It uses the Consultant class to generate a list of clarification questions based on the problem description.
    It returns a JSON object containing the list of clarification questions.
    """
    data = request.get_json()
    problem_description = data["problem-description"]
    consultant = Consultant()
    clarification_questions = consultant.get_clarification(problem_description)
    return jsonify({"questions": clarification_questions})


@app.route("/api/v1/consultant/solve", methods=["POST"])
def get_solution():
    """
    This method accepts a POST request with a JSON object containing a problem description, clarification answers, and number of solutions.
    It uses the Consultant class to generate a solution based on the problem description, clarification answers, and number of solutions.
    It returns a JSON object containing the solution.
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

import os
import logging
from flask import Flask
from flask import request, jsonify
from brainstorm.main import Consultant


app = Flask(__name__, static_folder='static')

log_level = os.environ.get('LOG_LEVEL', 'INFO')
logging.basicConfig(level=log_level)


@app.route('/api/v1/consultant/clarify', methods=['POST'])
def get_clarification():
    data = request.get_json()
    problem_description = data['problem-description']
    consultant = Consultant()
    clarification_questions = consultant.get_clarification(problem_description)
    return jsonify({'questions': clarification_questions})

@app.route('/api/v1/consultant/solve', methods=['POST'])
def get_solution():
    data = request.get_json()
    problem_description = data['problem-description']
    clarification_answers = data['clarification-answers']
    number_of_solutions = data.get('number-of-solutions', 3)
    consultant = Consultant()
    solution = consultant.get_solution(problem_description, clarification_answers, number_of_solutions)
    return jsonify({'solution': solution})

if __name__ == '__main__':
    app.run(debug=True)
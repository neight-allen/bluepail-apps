# Brainstorm

Brainstorm is a Flask app that provides a natural language interface for solving problems. It uses a machine learning model to generate questions that help clarify the problem, and then generates solutions based on the user's answers to those questions.

## Installation

To install Brainstorm, clone the repository and install the dependencies using pip:

```bash
git clone https://github.com/neight-allen/bluepail-apps/
cd bluepail-apps
```

Optionally, you can create and use a virtual environment to avoid installing the dependencies globally:

```bash
python -m venv venv
source venv/bin/activate
```

Then, install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage

To run the app, use the following command:

```
python app.py
```

This will start the Flask development server on port 5000. You can access the app by navigating to `http://localhost:5000` in your web browser.

## API

Brainstorm provides a REST API for accessing its functionality. The following endpoints are available:

- `/api/v1/consultant/clarify`: Generates clarification questions for a given problem description.
  - Example Payload:
    ```
    {
        "problem-description": "I'm having trouble understanding recursion in programming."
    }
    ```
  - Example Response:
    ```
    {
        "questions": [
            "What part of recursion do you find most confusing?",
            "Have you tried solving problems using recursion?",
            "Do you understand the concept of a base case in recursion?"
        ]
    }
    ```
- `/api/v1/consultant/solve`: Generates solutions for a given problem description and set of clarification answers.
  - Example Payload:
    ```
    {
        "problem-description": "I'm having trouble understanding recursion in programming.",
        "clarification-answers": [
            {
                "question": "What part of recursion do you find most confusing?",
                "answer": "I don't understand how the function calls itself without causing an infinite loop."
            },
            {
                "question": "Have you tried solving problems using recursion?",
                "answer": "Yes, but I always end up with stack overflow errors."
            },
            {
                "question": "Do you understand the concept of a base case in recursion?",
                "answer": "I think so, it's the condition that stops the recursion, right?"
            }
        ],
        "number-of-solutions": 3
    }
    ```
    
  - Example Response:
    ```
    {
        "solutions": [
            "Try visualizing the recursion with a diagram or a stack of cards to understand how it works.",
            "Practice with simple problems first, like calculating factorial or fibonacci numbers using recursion.",
            "Remember to always define a base case that will stop the recursion. Without it, you will indeed get an infinite loop and a stack overflow error."
        ]
    }
    ```

The `number-of-solutions` field is now mandatory and must be provided in the request.

## New Features

Error handling has been added to the `get_clarification` and `get_solution` methods. If an error occurs while generating the clarification questions or solutions, an error message will be logged and an empty list or string will be returned, respectively.

## License

Brainstorm is licensed under the MIT License. See `LICENSE` for more information.

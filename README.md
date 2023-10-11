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
- `/api/v1/consultant/solve`: Generates solutions for a given problem description and set of clarification answers.

Both endpoints accept POST requests with JSON data in the following format:

```
{
    "problem-description": "A description of the problem.",
    "clarification-answers": [
        {
            "question": "Clarification question",
            "answer": "Answer to question 1."
        },
        {...},
        ...
    ],
    "number-of-solutions": 3
}
```

The `number-of-solutions` field is optional and defaults to 3.

## License

Brainstorm is licensed under the MIT License. See `LICENSE` for more information.

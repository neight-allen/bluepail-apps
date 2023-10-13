# This is the version of the code from commit 5efb4653ad104a5fdf9bd261001823d379b4af4a
import logging

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate


class Consultant:
    """
    A class to represent a consultant who solves problems.
    """

    solution_prompt_template = """
Tavita is a consultant. She is a detail oriented, experienced, empathetic, genius solver of problems. She is meeting with a client who is facing a problem. Here is their conversation:

Client: {{problem_description}}.
{% for item in clarification_answers -%}
Tavita: {{ item.question }}
Client: {{ item.answer }}
{% endfor %}
Tavita takes notes diligently and thinks through the problem. She pauses to consider her options.
Tavita: I can think of a few different approaches you could take. Let me collect my thoughts an document them in an actionble manner for you. I'll email them by the end of the day.

Tavita writes up a report with the following summary of the client's problem, along with {{number_of_solutions}} actionable plans, formatted in markdown:
"""

    clarification_prompt_template = """Tavita is a consultant. She is a detail oriented, experienced, empathetic, genius solver of problems.

One of her clients is facing a problem. Here is how they describe the problem to Tavita: "{problem_description}".

As an expert, Tavita knows that the client may not have given her all the information she needs to solve the problem. So she asks exactly three clarifying questions, formatted here as a bulled list:

- """

    language_model = OpenAI(temperature=0.9)
    clarification_prompt = PromptTemplate(
        input_variables=["problem_description"], template=clarification_prompt_template
    )

    solution_prompt = PromptTemplate.from_template(
        template=solution_prompt_template, template_format="jinja2"
    )
    fewer_tokens = False
    logger = logging.getLogger(__name__)

    def format_clarification_prompt(self, problem_description):
        return self.clarification_prompt.format(problem_description=problem_description)

    def format_solution_prompt(
        self, problem_description, clarification_answers, number_of_solutions
    ):
        return self.solution_prompt.format(
            problem_description=problem_description,
            clarification_answers=clarification_answers,
            number_of_solutions=number_of_solutions,
        )

    def get_clarification(self, problem_description):
        try:
            formatted_clarification_prompt = self.format_clarification_prompt(
                problem_description
            )
            result = (
                " Just one question for you.\n- Ok, two."
                if self.fewer_tokens
                else self.language_model(formatted_clarification_prompt)
            )
            return [s.strip() for s in result.split("- ")]
        except Exception as e:
            self.logger.error(f"Error in get_clarification: {e}")
            return []

    def get_solution(
        self, problem_description, clarification_answers, number_of_solutions
    ):
        try:
            formatted_solution_prompt = self.format_solution_prompt(
                problem_description, clarification_answers, number_of_solutions
            )
            result = (
                "# Solution Report:\n\n## Problem statement: \n "
                + problem_description
                + "\n\n## Solutions: \n Just love yourself, and everything will be ok."
                if self.fewer_tokens
                else self.language_model(formatted_solution_prompt)
            )
            return result
        except Exception as e:
            self.logger.error(f"Error in get_solution: {e}")
            return ""



if __name__ == "__main__":
    consultant = Consultant()
    problem_description = "I need to market an upcoming conference. I have been involved in conference organizing before, and have a functional network of locals that would be interested, but I'm not very good at marketing. The conference would be a hackathon style weekend for building generative AI applications"
    print(consultant.get_clarification(problem_description))

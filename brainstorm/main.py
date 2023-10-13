import logging

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate


class Consultant:
    """
    The Consultant class is responsible for problem-solving and generating solutions. It uses the OpenAI language model to generate clarifications and solutions based on the problem description and clarification answers.
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

    llm = OpenAI(temperature=0.9)
    clarification_prompt = PromptTemplate(
        input_variables=["problem_description"], template=clarification_prompt_template
    )

    solution_prompt = PromptTemplate.from_template(
        template=solution_prompt_template, template_format="jinja2"
    )
    fewer_tokens = False
    logger = logging.getLogger(__name__)

    def get_clarification(self, problem_description):
        """
        Generates clarifying questions for the given problem description using the OpenAI language model. Returns a list of clarifying questions.

        Parameters:
        problem_description (str): The problem description.

        Returns:
        list: A list of clarifications.
        """
        formatted_clarification_prompt = self.clarification_prompt.format(
            problem_description=problem_description
        )
        self.logger.info(formatted_clarification_prompt)
        if self.fewer_tokens:
            result = " Just one question for you.\n- Ok, two."
        else:
            result = self.llm(formatted_clarification_prompt)
        self.logger.info(result)
        return [s.strip() for s in result.split("- ")]

    def get_solution(
        self, problem_description, clarification_answers, number_of_solutions
    ):
        """
        Generates a solution for the given problem description, clarification answers, and the number of solutions using the OpenAI language model. Returns the solution as a string.

        Parameters:
        problem_description (str): The problem description.
        clarification_answers (list): The clarification answers.
        number_of_solutions (int): The number of solutions.

        Returns:
        str: The solution.
        """
        self.logger.info("clarification_answers: %s", clarification_answers)
        formatted_solution_prompt = self.solution_prompt.format(
            problem_description=problem_description,
            clarification_answers=clarification_answers,
            number_of_solutions=number_of_solutions,
        )
        self.logger.info(formatted_solution_prompt)
        if self.fewer_tokens:
            result = (
                "# Solution Report:\n\n## Problem statement: \n "
                + problem_description
                + "\n\n## Solutions: \n Just love yourself, and everything will be ok."
            )
        else:
            result = self.llm(formatted_solution_prompt)
        self.logger.info(result)
        return result


if __name__ == "__main__":
    # Code to run if this file is being executed
    consultant = Consultant()

    print(
        consultant.get_clarification(
            "I need to market an upcoming conference. I have been involved in conference organizing before, and have a functional network of locals that would be interested, but I'm not very good at marketing. The conference would be a hackathon style weekend for buliding generative AI applications"
        )
    )

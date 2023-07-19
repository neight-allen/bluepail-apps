from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate


class Consultant():

    solution_prompt_template = """
Tavita is a consultant. She is a detail oriented, experienced, empathetic, genius solver of problems. She is meeting with a client who is facing a problem. Here is their conversation:

Client: {{problem_description}}.
{% for item in qs_and_as %}
Tavita: {{ item.question }}
Client: {{ item.answer }}
{% endfor %}
Tavita takes notes dilligently and thinks through the problem. She pauses to consider her options.
Tavita: I can think of a few different approaches you could take. Let me collect my thoughts an document them in an actionble manner for you. I'll email them by the end of the day.

Tavita writes up a report with the following summary of the client's problem, along with {{number_of_solutions}} actionable plans:
"""

    clarification_prompt_template = """Tavita is a consultant. She is a detail oriented, experienced, empathetic, genius solver of problems.

One of her clients is facing a problem. Here is how they describe the problem to Tavita: "{problem_description}".

As an expert, Tavita knows that the client may not have given her all the information she needs to solve the problem. So she asks the following clarifying questions, formatted here as a bulled list:

- """

    llm = OpenAI(temperature=0.9)
    clarification_prompt = PromptTemplate(
        input_variables=["problem_description"], template=clarification_prompt_template
    )

    solution_prompt = PromptTemplate.from_template(
        # input_variables=["qs_and_as","problem_statement","number_of_solutions"], 
        template=solution_prompt_template, template_format="jinja2"
    )

    def get_clarification(self, problem_description):
        formatted_clarification_prompt = self.clarification_prompt.format(problem_description=problem_description)
        print(formatted_clarification_prompt)
        result = self.llm(formatted_clarification_prompt)
        print(result)
        return [s.strip() for s in result.split("- ")]

if __name__ == "__main__":
    # Code to run if this file is being executed
    consultant = Consultant()

    print(consultant.get_clarification("I need to market an upcoming conference. I have been involved in conference organizing before, and have a functional network of locals that would be interested, but I'm not very good at marketing. The conference would be a hackathon style weekend for buliding generative AI applications"))
from openai import OpenAI
import os
from dotenv import load_dotenv
import tools
import json
import prompts

load_dotenv('.env')
openai_api_key = os.getenv("OPENAI_API_KEY")

def assemble_prompt(subject, level, question, suggested_answer, marks, student_response, prompt_template=prompts.SA_prompt):
    user_message = prompt_template.format(Subject=subject, Level=level, Question=question, Model_answer=suggested_answer, Marks=marks, Students_response=student_response)
    return user_message

def evaluate(user_prompt):
    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        temperature = 0.1,
        max_tokens = 16000,
        tools = tools.SA_Tools,
        messages=[{"role": "user", "content":user_prompt}]
        )
    feedback_and_marks = response.choices[0].message.tool_calls[0].function.arguments
    dict_feedback_and_marks = json.loads(feedback_and_marks)
    print("Awarded marks: " + str(dict_feedback_and_marks["answer_scheme_marks"]))
    print("Feedback: \n" + dict_feedback_and_marks["general_feedback"])
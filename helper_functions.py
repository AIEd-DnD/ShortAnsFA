from openai import OpenAI
import os
import csv
from dotenv import load_dotenv
from datetime import datetime
import tools
import json
import prompts

load_dotenv('.env')
openai_api_key = os.getenv("OPENAI_API_KEY")

def start_new_SA_record(file_name):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Records/ShortAnsFA_SA_{file_name}_{timestamp}.csv"
    return filename

def start_new_Rubric_record(file_name):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Records/ShortAnsFA_Rubric_{file_name}_{timestamp}.csv"
    return filename

def SA_write_into_record(filename, data):
    header = ['Subject','Level','Question','Student Response','Suggested Answer','Instructions','Maximum Marks','Expected Marks','Awarded Marks','Mark Variance','Feedback',]
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)
    print(f"CSV file '{filename}' has been created successfully.")

def Rubric_write_into_record(filename, data):
    header = ['Subject','Level','Question','Student Response','Rubric','Instructions','Maximum Marks','Expected Marks','Awarded Marks','Mark Variance','Feedback',]
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)
    print(f"CSV file '{filename}' has been created successfully.")

def csv_to_list_of_dicts(file_path):
    result = list()
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            result.append(row)
    return result

def SA_extract_parameters(parameter_dict):
    subject = parameter_dict['subject']
    level = parameter_dict['level']
    question = parameter_dict['question']
    students_response = parameter_dict['students_response']
    suggested_answer = parameter_dict['suggested_answer']
    instructions = parameter_dict['instructions']
    max_marks = parameter_dict['maximum_marks']
    exp_marks = parameter_dict['expected_marks']
    return subject, level, question, students_response, suggested_answer, instructions, max_marks, exp_marks

def Rubric_extract_parameters(parameter_dict):
    subject = parameter_dict['subject']
    level = parameter_dict['level']
    question = parameter_dict['question']
    students_response = parameter_dict['students_response']
    rubric = parameter_dict['rubric']
    instructions = parameter_dict['instructions']
    max_marks = parameter_dict['maximum_marks']
    exp_marks = parameter_dict['expected_marks']
    return subject, level, question, students_response, rubric, instructions, max_marks, exp_marks

def assemble_SA_prompt(subject, level, question, suggested_answer, marks, instructions, student_response, prompt_template=prompts.SA_prompt_v1):
    user_message = prompt_template.format(Subject=subject, Level=level, Question=question, Model_answer=suggested_answer, Marks=marks, Instructions=instructions, Students_response=student_response)
    return user_message

def assemble_Rubric_prompt(subject, level, question, rubric, marks, instructions, student_response, prompt_template=prompts.rubrics_prompt_v1):
    user_message = prompt_template.format(Subject=subject, Level=level, Question=question, Rubrics_marking=rubric, Marks=marks, Instructions=instructions, Students_response=student_response)
    return user_message

def assemble_prompt(subject, level, question, rubrics, suggested_answer, marks, student_response, prompt_template=prompts.base_prompt):
    user_message = prompt_template.format(Subject=subject, Level=level, Question=question, Rubrics_marking=rubrics, Model_answer=suggested_answer, Marks=marks, Students_response=student_response)
    return user_message

def evaluate(user_prompt):
    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        #model="o3-mini",
        temperature = 0.1,
        max_tokens = 4000,
        #max_completion_tokens=50000,
        tools = tools.full_tools,
        messages=[{"role": "user", "content":user_prompt}]
        )
    #print(response)
    return response

def evaluate_SA(user_prompt):
    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        #model="o3-mini",
        temperature = 0.1,
        max_tokens = 4000,
        #max_completion_tokens=50000,
        tools = tools.SA_Tools,
        messages=[{"role": "user", "content":user_prompt}]
        )
    #print(response)
    return response

def evaluate_Rubric(user_prompt):
    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        temperature = 0.1,
        max_tokens = 4000,
        tools = tools.rubrics_Tools_v1,
        messages=[{"role": "user", "content":user_prompt}]
        )
    return response

def extract_feedback_and_marks(response):
    feedback_and_marks = response.choices[0].message.tool_calls[0].function.arguments
    dict_feedback_and_marks = json.loads(feedback_and_marks)
    awarded_marks = str(dict_feedback_and_marks["answer_scheme_marks"])
    general_feedback = dict_feedback_and_marks["general_feedback"]
    return awarded_marks, general_feedback

def extract_SA_feedback_and_marks(response):
    feedback_and_marks = response.choices[0].message.tool_calls[0].function.arguments
    dict_feedback_and_marks = json.loads(feedback_and_marks)
    awarded_marks = str(dict_feedback_and_marks["awarded_marks"])
    general_feedback = dict_feedback_and_marks["general_feedback"]
    return awarded_marks, general_feedback

def extract_Rubric_feedback_and_marks(response):
    feedback_and_marks = response.choices[0].message.tool_calls[0].function.arguments
    dict_feedback_and_marks = json.loads(feedback_and_marks)
    total_awarded_marks = 0
    for rubric in dict_feedback_and_marks["rubrics"]:
        total_awarded_marks += rubric["dimension_marks"]
    awarded_marks = str(total_awarded_marks)
    feedback_container = []
    for rubric in dict_feedback_and_marks["rubrics"]:
        dimensionId = rubric["dimensionId"]
        dimension_feedback = rubric["rubrics_feedback"]
        feedback_container.append(f"Dimension {dimensionId}: {dimension_feedback}")
    general_feedback = "\n".join(feedback_container)
    return awarded_marks, general_feedback

def display_feedback_and_marks(awarded_marks, general_feedback):
    print("Awarded marks: " + awarded_marks)
    print("Feedback: \n" + general_feedback)
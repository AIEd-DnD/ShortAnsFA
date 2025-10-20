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

def start_new_accuracy_record(file_name):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Records/ShortAnsFA_Accuracy_{file_name}_{timestamp}.csv"
    return filename

def SA_write_into_record(filename, data):
    header = ['s/n','Condition','Subject','Level','Question','Student Response','Suggested Answer','Instructions','Maximum Marks','Expected Marks','Awarded Marks','Mark Variance','Feedback',]
    with open(filename, 'w', newline='',encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)
    print(f"CSV file '{filename}' has been created successfully.")

def Rubric_write_into_record(filename, data):
    header = ['s/n','Condition','Subject','Level','Question','Student Response','Rubric','Instructions','Maximum Marks','Expected Marks','Awarded Marks','Mark Variance','Feedback',]
    with open(filename, 'w', newline='',encoding='utf-8-sig') as file:
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
    condition = parameter_dict['condition']
    subject = parameter_dict['subject']
    level = parameter_dict['level']
    question = parameter_dict['question']
    students_response = parameter_dict['students_response']
    suggested_answer = parameter_dict['suggested_answer']
    instructions = parameter_dict['instructions']
    max_marks = parameter_dict['maximum_marks']
    exp_marks = parameter_dict['expected_marks']
    return condition, subject, level, question, students_response, suggested_answer, instructions, max_marks, exp_marks

def Rubric_extract_parameters(parameter_dict):
    condition = parameter_dict['condition']
    subject = parameter_dict['subject']
    level = parameter_dict['level']
    question = parameter_dict['question']
    students_response = parameter_dict['students_response']
    rubric = parameter_dict['rubric']
    instructions = parameter_dict['instructions']
    max_marks = parameter_dict['maximum_marks']
    exp_marks = parameter_dict['expected_marks']
    return condition, subject, level, question, students_response, rubric, instructions, max_marks, exp_marks

def assemble_SA_prompt_split_all_part1(subject, level, prompt_template=prompts.SAFA_SA_Split_All_part_1_v2):
    user_message_part_1 = prompt_template.format(Subject=subject, Level=level)
    return user_message_part_1

def assemble_SA_prompt_split_all_part3(level, marks, instructions, prompt_template=prompts.SAFA_SA_Split_All_part_3_v2):
    user_message_part_3 = prompt_template.format(Level=level, Marks=marks, Instructions=instructions)
    return user_message_part_3

def assemble_Rubric_prompt(subject, level, question, rubric, marks, instructions, student_response, prompt_template=prompts.SAFA_SA):
    user_message = prompt_template.format(Subject=subject, Level=level, Question=question, Rubrics_marking=rubric, Marks=marks, Instructions=instructions, Students_response=student_response)
    return user_message

def assemble_Rubric_prompt_split_all_part1(subject, level, prompt_template=prompts.SAFA_Rubric_Split_All_part_1):
    user_message_part_1 = prompt_template.format(Subject=subject, Level=level)
    return user_message_part_1

def assemble_Rubric_prompt_split_all_part2(rubrics_marking, level, marks, instructions, prompt_template=prompts.SAFA_Rubric_Split_All_part_2):
    user_message_part_2 = prompt_template.format(Rubrics_marking=rubrics_marking, Level=level, Marks=marks, Instructions=instructions)
    return user_message_part_2

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
        tools = tools.SA_Tools_v1,
        messages=[{"role": "user", "content":user_prompt}]
        )
    #print(response)
    return response

def message_builder(user_prompt_part_1, qn, user_prompt_part_2, sa, user_prompt_part_3, response, user_prompt_part_4):
    content_array = list()
    if any(ext in response for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]) and any(ext in sa for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]) and any(ext in qn for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]): 
        #print("All three are images")
        content_array = [
                            {"type":"text", "text":user_prompt_part_1},
                            {"type":"image_url", "image_url":{"url":qn, "detail":"low"}},
                            {"type":"text", "text":user_prompt_part_2},
                            {"type":"image_url", "image_url":{"url":sa, "detail":"low"}},
                            {"type":"text", "text":user_prompt_part_3},
                            {"type":"image_url", "image_url":{"url":response, "detail":"low"}},
                            {"type":"text", "text":user_prompt_part_4}
                        ]
        return content_array
    elif any(ext in response for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]) and any(ext in sa for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]) and any(ext not in qn for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]): 
        #print("Response and SA are images")
        content_array = [
                            {"type":"text", "text":user_prompt_part_1 + qn + user_prompt_part_2},
                            {"type":"image_url", "image_url":{"url":sa, "detail":"low"}},
                            {"type":"text", "text":user_prompt_part_3},
                            {"type":"image_url", "image_url":{"url":response, "detail":"low"}},
                            {"type":"text", "text":user_prompt_part_4}
                        ]
        return content_array
    elif any(ext in response for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]) and any(ext not in sa for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]) and any(ext in qn for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]): 
        #print("Response and Qn are images")
        content_array = [
                            {"type":"text", "text":user_prompt_part_1},
                            {"type":"image_url", "image_url":{"url":qn, "detail":"low"}},
                            {"type":"text", "text":user_prompt_part_2 + sa + user_prompt_part_3},
                            {"type":"image_url", "image_url":{"url":response, "detail":"low"}},
                            {"type":"text", "text":user_prompt_part_4}
                        ]
        return content_array
    elif any(ext not in response for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]) and any(ext in sa for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]) and any(ext in qn for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]): 
        #print("SA and Qn are images")
        content_array = [
                            {"type":"text", "text":user_prompt_part_1},
                            {"type":"image_url", "image_url":{"url":qn, "detail":"low"}},
                            {"type":"text", "text":user_prompt_part_2},
                            {"type":"image_url", "image_url":{"url":sa, "detail":"low"}},
                            {"type":"text", "text":user_prompt_part_3 + response + user_prompt_part_4}
                        ]
        return content_array
    elif any(ext in response for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]) and any(ext not in sa for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]) and any(ext not in qn for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]): 
        #print("Only response is image")
        content_array = [
                            {"type":"text", "text":user_prompt_part_1 + qn + user_prompt_part_2 + sa + user_prompt_part_3},
                            {"type":"image_url", "image_url":{"url":response, "detail":"low"}},
                            {"type":"text", "text":user_prompt_part_4}
                        ]
        return content_array
    elif any(ext not in response for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]) and any(ext in sa for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]) and any(ext not in qn for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]): 
        #print("Only SA is image")
        content_array = [
                            {"type":"text", "text":user_prompt_part_1 + qn + user_prompt_part_2},
                            {"type":"image_url", "image_url":{"url":sa, "detail":"low"}},
                            {"type":"text", "text":user_prompt_part_3 + response + user_prompt_part_4}
                        ]
        return content_array
    elif any(ext not in response for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]) and any(ext not in sa for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]) and any(ext in qn for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]): 
        #print("Only Qn is image")
        content_array = [
                            {"type":"text", "text":user_prompt_part_1},
                            {"type":"image_url", "image_url":{"url":qn, "detail":"low"}},
                            {"type":"text", "text":user_prompt_part_2 + sa + user_prompt_part_3 + response + user_prompt_part_4}
                        ]
        return content_array
    else:
        content = user_prompt_part_1 + qn + user_prompt_part_2 + sa + user_prompt_part_3 + response + user_prompt_part_4
        return content

def message_builder_Rubric(user_prompt_part_1, qn, user_prompt_part_2, response, user_prompt_part_3):
    content_array = list()
    if any(ext in response for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]) and any(ext in qn for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]): 
        content_array = [
                            {"type":"text", "text":user_prompt_part_1},
                            {"type":"image_url", "image_url":{"url":qn, "detail":"low"}},
                            {"type":"text", "text":user_prompt_part_2},
                            {"type":"image_url", "image_url":{"url":response, "detail":"low"}},
                            {"type":"text", "text":user_prompt_part_3},
                        ]
        return content_array
    elif any(ext in response for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]) and any(ext not in qn for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]): 
        content_array = [
                            {"type":"text", "text":user_prompt_part_1 + qn + user_prompt_part_2},
                            {"type":"image_url", "image_url":{"url":response, "detail":"low"}},
                            {"type":"text", "text":user_prompt_part_3}
                        ]
        return content_array
    elif any(ext not in response for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]) and any(ext in qn for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]): 
        content_array = [
                            {"type":"text", "text":user_prompt_part_1},
                            {"type":"image_url", "image_url":{"url":qn, "detail":"low"}},
                            {"type":"text", "text":user_prompt_part_2 + response + user_prompt_part_3}
                        ]
        return content_array
    else:
        content = user_prompt_part_1 + qn + user_prompt_part_2 + response + user_prompt_part_3
        return content

def evaluate_SA_split_all(user_prompt_part_1, qn, sa, user_prompt_part_3, response, user_prompt_part_2=prompts.SAFA_SA_Split_All_part_2_v2, user_prompt_part_4=prompts.SAFA_SA_Split_All_part_4_v2):
    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        #model="o3-mini",
        temperature = 0.1,
        max_tokens = 4000,
        #max_completion_tokens=50000,
        tools = tools.SA_Tools_v1,
        messages=[{"role": "user", 
                   "content":message_builder(user_prompt_part_1, qn, user_prompt_part_2, sa, user_prompt_part_3, response, user_prompt_part_4)
                    }
                ]
        )
    #print(response)
    return response

def evaluate_Rubric_split_all(user_prompt_part_1, qn, user_prompt_part_2, response, user_prompt_part_3=prompts.SAFA_Rubric_Split_All_part_3):
    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        #model="o3-mini",
        temperature = 0.1,
        max_tokens = 4000,
        #max_completion_tokens=50000,
        tools = tools.rubrics_Tools_v1,
        messages=[{"role": "user", 
                   "content":message_builder_Rubric(user_prompt_part_1, qn, user_prompt_part_2, response, user_prompt_part_3)
                    }
                ]
        )
    #print(response)
    return response

def evaluate_SA_gpt5(user_prompt):
    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-5-2025-08-07",
        reasoning_effort="high",
        max_completion_tokens=32000,
        tools = tools.SA_Tools_v1,
        messages=[{"role": "user", "content":user_prompt}]
        )
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

def evaluate_Rubric_gpt5(user_prompt):
    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-5-2025-08-07",
        reasoning_effort="high",
        max_completion_tokens=32000,
        tools = tools.rubrics_Tools,
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

def ShortAnsFA_Accuracy_write_into_record(filename, data):
    header = ['Condition','Maximum Marks','Expected Marks','Average Awarded Marks','Average Mark Variance']
    with open(filename, 'w', newline='',encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)
    print(f"CSV file '{filename}' has been created successfully.")

def Accuracy_extract_parameters(parameter_dict):
    condition = parameter_dict['Condition']
    max_marks = parameter_dict['Maximum Marks']
    exp_marks = parameter_dict['Expected Marks']
    awarded_marks = parameter_dict['Awarded Marks']
    mark_variance = parameter_dict['Mark Variance'] 
    return condition, max_marks, exp_marks, awarded_marks, mark_variance
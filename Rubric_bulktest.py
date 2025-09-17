import helper_functions as SAFA

data = list()
#test_name = input("Please enter the name of the test: ")               #uncomment this to unlock user input for test name
#file_path = input("Please enter the file path of the test data: ")     #uncomment this to unlock user input for file path
evaluation_record = SAFA.start_new_Rubric_record("BulkEval_Test_split_newprompt_newtools_GPT5")
print("The evaluation record has been created.")
response_list = SAFA.csv_to_list_of_dicts("Dataset/BulkTest_SAFA_Rubrics.csv")
print("The response list has been created.")
rubric = ' '

for scenario_dict in response_list:
    new_row = list()
    subject, level, question, students_response, rubric, instructions, max_marks, exp_marks = SAFA.Rubric_extract_parameters(scenario_dict)
    
    new_row.append(subject)
    new_row.append(level)
    new_row.append(question)
    new_row.append(students_response)
    new_row.append(rubric)
    new_row.append(instructions)
    new_row.append(max_marks)
    new_row.append(exp_marks)

    print('Trying response '+str(response_list.index(scenario_dict)+1)+' out of '+str(len(response_list)))

    user_prompt = SAFA.assemble_Rubric_prompt(subject, level, question, rubric, max_marks, instructions, students_response)
    #print(user_prompt)
    response = SAFA.evaluate_Rubric_gpt5(user_prompt)
    #print(response)
    awarded_marks, general_feedback = SAFA.extract_Rubric_feedback_and_marks(response)
    
    int_awarded_marks = int(awarded_marks)
    int_exp_marks = int(exp_marks)
    variance = int_exp_marks - int_awarded_marks #positive variance means too strict, negative variance means too lenient
    
    new_row.append(awarded_marks)
    new_row.append(variance)
    new_row.append(general_feedback)

    data.append(new_row)

SAFA.Rubric_write_into_record(evaluation_record, data)
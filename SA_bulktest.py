import helper_functions as SAFA

data = list()
#test_name = input("Please enter the name of the test: ")               #uncomment this to unlock user input for test name
#file_path = input("Please enter the file path of the test data: ")     #uncomment this to unlock user input for file path
evaluation_record = SAFA.start_new_SA_record("BulkEval_SAFA_SuggestedAnswer_prompt_v2_tools_v1_FeedbackSample")
print("The evaluation record has been created.")
response_list = SAFA.csv_to_list_of_dicts("Dataset/BulkTest_SAFA_SuggestedAnswer_TestBench_v2.csv")
print("The response list has been created.")
repeats_per_response = 1

for scenario_dict in response_list:
    for i in range(repeats_per_response):
        new_row = list()
        condition, subject, level, question, students_response, suggested_answer, instructions, max_marks, exp_marks = SAFA.SA_extract_parameters(scenario_dict)
    
        new_row.append(i+1)  #serial number for each run
        new_row.append(condition)
        new_row.append(subject)
        new_row.append(level)
        new_row.append(question)
        new_row.append(students_response)
        new_row.append(suggested_answer)
        new_row.append(instructions)
        new_row.append(max_marks)
        new_row.append(exp_marks)

        print('Trying response '+str(response_list.index(scenario_dict)+1)+' out of '+str(len(response_list))+' (Run '+str(i+1)+' out of '+str(repeats_per_response)+')')

        #user_prompt = SAFA.assemble_SA_prompt(subject, level, question, suggested_answer, max_marks, instructions, students_response)
        #print(user_prompt)
        user_prompt_part_1 = SAFA.assemble_SA_prompt_split_all_part1(subject, level)
        user_prompt_part_3 = SAFA.assemble_SA_prompt_split_all_part3(level, max_marks, instructions)


        #response = SAFA.evaluate_SA_gpt5(user_prompt)
        response = SAFA.evaluate_SA_split_all(user_prompt_part_1, question, suggested_answer, user_prompt_part_3, students_response)
        #print(response)
        awarded_marks, general_feedback = SAFA.extract_feedback_and_marks(response)
    
        int_awarded_marks = int(awarded_marks)
        int_exp_marks = int(exp_marks)
        variance = int_exp_marks - int_awarded_marks #positive variance means too strict, negative variance means too lenient
    
        new_row.append(awarded_marks)
        new_row.append(variance)
        new_row.append(general_feedback)

        data.append(new_row)

SAFA.SA_write_into_record(evaluation_record, data)
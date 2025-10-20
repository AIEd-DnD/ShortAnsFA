import helper_functions as SAFA

data = list()
#test_name = input("Please enter the name of the test: ")               #uncomment this to unlock user input for test name
#file_path = input("Please enter the file path of the test data: ")     #uncomment this to unlock user input for file path
evaluation_record = SAFA.start_new_accuracy_record("SAFA_Rubric_prompt_v1_tools_v1")
print("The evaluation record has been created.")
response_list = SAFA.csv_to_list_of_dicts("Records/ShortAnsFA_Rubric_BulkEval_SAFA_Rubric_prompt_v1_tools_v1_20251016_180058.csv")
print("The response list has been created.")
repeats_per_response = 10
testbench_size = int(len(response_list)/repeats_per_response)
start = 0
end = repeats_per_response

for test in range(testbench_size):
    new_row = list()
    sum_awarded = 0
    sum_variance = 0
    for run in response_list[start:end]:
        condition, max_marks, exp_marks, awarded_marks, mark_variance = SAFA.Accuracy_extract_parameters(run)
        sum_awarded += int(awarded_marks)
        sum_variance += int(mark_variance)
    mean_awarded = sum_awarded / repeats_per_response
    mean_variance_sq = (sum_variance / repeats_per_response) ** 2

    new_row.append(condition)
    new_row.append(max_marks)
    new_row.append(exp_marks)
    new_row.append(round(mean_awarded,2))
    new_row.append(round(mean_variance_sq,2))
    data.append(new_row)
    start += repeats_per_response
    end += repeats_per_response

SAFA.ShortAnsFA_Accuracy_write_into_record(evaluation_record, data)

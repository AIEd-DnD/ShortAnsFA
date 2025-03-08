import helper_functions as SAFA

### SA ShortAnsFA
subject = "Physics"
level = "Secondary 4"
question = "Explain how the circuit breaker breaks the circuit."
rubrics = " "
suggested_answer = "(1 mark): The current flowing through the coil causes it to become an electromagnet, which exerts a [downward] / [attracting] / [pulling] force on the iron arm. \n (1 mark): The magnetic force becomes greater as the current flowing through the coil increases. \n (1 mark): When the [current increases beyond 30 A], the force becomes great enough to separate the lower contact from the upper contact, thereby breaking the circuit. <additional marking instructions> No mark awarded if student does not state the direction (downward, attracted, pulling) of exerted force. No mark awarded if student not specify the critical current of 30A.</additional marking instructions> "
marks = "3"
student_response = "The current flowing through the coil turn it into an electromagnet, which exerts a force on the iron arm. When the current is greater than 30 A, the force becomes great enough to separate the lower contact from the upper contact, thereby breaking the circuit."

print("Split Prompt Results")
for i in range(10):
    user_prompt = SAFA.assemble_SA_prompt(subject, level, question, suggested_answer, marks, student_response)
    response = SAFA.evaluate_SA(user_prompt)
    awarded_marks, general_feedback = SAFA.extract_SA_feedback_and_marks(response)
    SAFA.display_SA_feedback_and_marks(awarded_marks, general_feedback)

print(" ")
print("Standard Prompt Results")
for e in range(10):
    user_prompt_standard = SAFA.assemble_prompt(subject, level, question, rubrics, suggested_answer, marks, student_response)
    respose_standard = SAFA.evaluate(user_prompt_standard)
    awarded_standard_marks, general_standard_feedback = SAFA.extract_SA_feedback_and_marks(respose_standard)
    SAFA.display_SA_feedback_and_marks(awarded_standard_marks, general_standard_feedback)

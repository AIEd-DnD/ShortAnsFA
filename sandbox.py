import helper_functions as SAFA

### SA ShortAnsFA
subject = "Physics"
level = "Secondary 4"
question = "Explain how the circuit breaker breaks the circuit."
suggested_answer = "(1 mark): The current flowing through the coil causes it to become an electromagnet, which exerts a [downward] / [attracting] / [pulling] force on the iron arm. \n (1 mark): The magnetic force becomes greater as the current flowing through the coil increases. \n (1 mark): When the [current increases beyond 30 A], the force becomes great enough to separate the lower contact from the upper contact, thereby breaking the circuit. "
marks = "3"
student_response = "The current flowing through the coil turns it into an electromagnet, which exerts a  force on the iron arm. The force becomes great enough to separate the lower contact from the upper contact, thereby breaking the circuit."



user_prompt = SAFA.assemble_SA_prompt(subject, level, question, suggested_answer, marks, student_response)
response = SAFA.evaluate_SA(user_prompt)
awarded_marks, general_feedback = SAFA.extract_SA_feedback_and_marks(response)
SAFA.display_SA_feedback_and_marks(awarded_marks, general_feedback)
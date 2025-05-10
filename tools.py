full_tools = [
  {
    "type": "function",
    "function": {
      "name": "get_marks_feedback_and_rubrics",
      "description": "Evaluate and must return marks, general_feedback and rubrics in a list format with the properties required in a JSON object",
      "parameters": {
        "type": "object",
        "properties": {
          "answer_scheme_marks": {
            "type": "integer",
            "description": "Total marks generated from the answer schema"
          },
          "general_feedback": {
            "type": "string",
            "description": "Generate feedback in details using suggested answer as reference and given in a first person perspective."
          },
          "rubrics": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "dimension_marks": {
                  "type": "integer"
                },
                "dimensionId": {
                  "type": "integer",
                  "description": "dimension id"
                },
                "rubrics_feedback": {
                  "type": "string",
                  "description": "Response after referencing criterion and given in a first person perspective only other than marks returned."
                }
              }
            },
            "description": "Return the list of rubrics responses with marks, dimensionId and rubrics_feedback"
          }
        },
        "required": [
          "answer_scheme_marks",
          "general_feedback",
          "rubrics"
        ]
      }
    }
  }
]

SA_Tools = [
        {
            "type": "function",
            "function": {
                "name": "get_marks_and_feedback",
                "description": "Evaluate and must return marks and general_feedback in a list format with the properties required in a JSON object",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "answer_scheme_marks": {
                            "type": "integer",
                            "description": "Total marks generated from the answer schema"
                        },
                        "general_feedback": {
                            "type": "string",
                            "description": "Generate feedback in details using suggested answer as reference and given in a first person perspective."
                        },
                    },
                    "required": [
                        "answer_scheme_marks",
                        "general_feedback"
                    ]
                }
            }
        }
    ]

SA_Tools_v1 = [
  {
    "type": "function",
    "function": {
      "name": "get_marks_and_feedback",
      "description": "Return awarded_marks and general_feedback in a list format with the properties required in a JSON object",
      "parameters": {
        "type": "object",
        "properties": {
          "awarded_marks": {
            "type": "integer",
            "description": "Final awarded marks given to the student's response according to the Grading Instructions."
          },
          "general_feedback": {
            "type": "string",
            "description": "Generated formative feedback to the student's response according to the Grading Instructions."
          }},
        "required": [
          "awarded_marks",
          "general_feedback"
        ]
      }
    }
  }
]


rubrics_Tools = [
        {
            "type": "function",
            "function": {
                "name": "get_marks_feedback_and_rubrics",
                "description": "Evaluate and must return marks, general_feedback and rubrics in a list format with the properties required in a JSON object",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "answer_scheme_marks": {
                            "type": "integer",
                            "description": "Total marks generated from the answer schema"
                        },
                        "rubrics": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "dimension_marks": {
                                        "type": "integer"
                                    },
                                    "dimensionId": {
                                        "type": "integer",
                                        "description": "dimension id"
                                    },
                                    "rubrics_feedback": {
                                        "type": "string",
                                        "description": "Response after referencing criterion and given in a first person perspective only other than marks returned."
                                    }
                                }
                            },
                            "description": "Return the list of rubrics responses with marks, dimensionId and rubrics_feedback"
                        }
                    },
                    "required": [
                        "answer_scheme_marks",
                        "rubrics"
                    ]
                }
            }
        }
    ]

rubrics_Tools_v1 = [
    {
    "type": "function",
    "function": {
      "name": "get_rubrics_marks_and_feedback",
      "description": "Return rubrics in a list format with the properties required in a JSON object",
      "parameters": {
        "type": "object",
        "properties": {
            "rubrics": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "dimension_marks": {
                  "type": "integer",
                  "description":"Final awarded marks for the Dimension given to the student's response according to the Grading Instructions."
                },
                "dimensionId": {
                  "type": "integer",
                  "description": "Dimension ID"
                },
                "rubrics_feedback": {
                  "type": "string",
                  "description": "Generated formative feedback for the Dimension to the student's response according to the Grading Instructions."
                }
              }
            },
            "description": "Return the list of rubrics Dimension responses with dimension_marks, dimensionId and rubrics_feedback for every Dimension in the Rubric"
          }
        },
        "required": [
          "rubrics"
        ]
      }
    }
  }
]
from crewai import Task

def create_question_task(agent, question_index, total_questions):
    return Task(
        description=f"""Ask interview question #{question_index + 1} of {total_questions}.
        The question should be clear, relevant, and specific to the role.""",
        agent=agent,
        expected_output="A clear, professional interview question"
    )

def create_feedback_task(agent, question, answer):
    return Task(
        description=f"""
        Question asked: {question}
        Candidate's answer: {answer}
        
        Provide short, constructive feedback (1-2 sentences) on this answer.
        Be specific - mention what was good and what could be improved.
        """,
        agent=agent,
        expected_output="Brief, constructive feedback on the candidate's answer"
    )
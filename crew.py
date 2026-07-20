from crewai import Crew, Process
from agents import question_agent, feedback_agent
from tasks import create_question_task, create_feedback_task

def run_interview_question(question, answer=None):
    if answer is None:
        return {"question": question, "feedback": None}
    else:
        task = create_feedback_task(feedback_agent, question, answer)
        
        crew = Crew(
            agents=[feedback_agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        feedback = str(result)
        
        return {"question": question, "feedback": feedback}
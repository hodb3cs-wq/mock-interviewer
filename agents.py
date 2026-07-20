from crewai import Agent

# ============================================
# CHOOSE YOUR ROLE - Change this line!
# ============================================

ROLE_TYPE = "DATA_SCIENTIST"  # Change to: WEB_DEVELOPER, PRODUCT_MANAGER, UI_UX_DESIGNER

# ============================================
# ROLE-SPECIFIC QUESTIONS
# ============================================

def get_role_questions(role):
    """Returns 5-6 interview questions for the selected role"""
    
    questions = {
        "DATA_SCIENTIST": [
            "What is overfitting in machine learning and how do you prevent it?",
            "Explain the difference between regression and classification algorithms.",
            "What is the purpose of cross-validation in model evaluation?",
            "How do you handle missing or null values in a dataset?",
            "Explain the bias-variance tradeoff in machine learning.",
            "What is the difference between supervised and unsupervised learning?"
        ],
        
        "WEB_DEVELOPER": [
            "Explain the difference between HTTP and HTTPS.",
            "What is the DOM and how do you manipulate it?",
            "Explain the concept of responsive web design.",
            "What is the difference between SQL and NoSQL databases?",
            "How does authentication work in web applications?",
            "Explain the MVC architecture in web development."
        ],
        
        "PRODUCT_MANAGER": [
            "How do you prioritize features in a product roadmap?",
            "Explain the difference between a product manager and a project manager.",
            "How do you gather and validate customer feedback?",
            "What metrics would you track to measure product success?",
            "How do you handle conflicting stakeholder requirements?",
            "Describe your approach to launching a new product feature."
        ],
        
        "UI_UX_DESIGNER": [
            "Explain the difference between UI and UX design.",
            "What is the importance of user research in design?",
            "How do you create a design system?",
            "Explain the concept of responsive design in UI/UX.",
            "What tools do you use for prototyping and why?",
            "How do you conduct usability testing?"
        ]
    }
    
    return questions.get(role, questions["DATA_SCIENTIST"])

# ============================================
# CREATE AGENTS
# ============================================

role_questions = get_role_questions(ROLE_TYPE)
role_name = ROLE_TYPE.replace("_", " ").title()

# AGENT 1: Question Generator
question_agent = Agent(
    role="Question Generator",
    goal=f"Ask exactly 5-6 interview questions for the {role_name} role",
    backstory=f"""You are an expert technical interviewer specializing in {role_name} roles.
    You ask relevant, challenging questions that test both theoretical knowledge and practical skills.
    Your questions should be clear, professional, and specific to {role_name} positions.""",
    verbose=True,
    allow_delegation=False
)

# AGENT 2: Feedback Agent
feedback_agent = Agent(
    role="Feedback Provider",
    goal="Provide constructive, short feedback on candidate's answers",
    backstory="""You are an experienced hiring manager with decades of interview experience.
    You provide concise, helpful feedback that guides candidates to improve.
    Your feedback is encouraging but honest, highlighting both strengths and areas for improvement.
    Keep feedback to 1-2 sentences maximum.""",
    verbose=True,
    allow_delegation=False
)

def get_questions_list():
    return role_questions

def get_role_display_name():
    return role_name
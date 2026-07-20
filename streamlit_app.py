import streamlit as st
import os
from agents import get_questions_list, get_role_display_name, ROLE_TYPE
from crew import run_interview_question

# Page configuration
st.set_page_config(
    page_title="AI Mock Interviewer",
    page_icon="🎯",
    layout="wide"
)

# Initialize session state
if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0
    st.session_state.questions = get_questions_list()
    st.session_state.answers = []
    st.session_state.feedback = []
    st.session_state.interview_started = False
    st.session_state.interview_complete = False
    st.session_state.current_answer = ""

# Header
st.title("🎯 AI-Powered Mock Interviewer")
st.markdown(f"### Role: **{get_role_display_name()}**")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("📊 Interview Progress")
    
    total_questions = len(st.session_state.questions)
    answered = len(st.session_state.answers)
    
    if total_questions > 0:
        progress = answered / total_questions
        st.progress(progress)
        st.write(f"**Questions Answered:** {answered}/{total_questions}")
    
    st.markdown("---")
    st.header("📌 Instructions")
    st.write("""
    1. Click **"Start Interview"**
    2. Read each question
    3. Type your answer
    4. Click **"Submit Answer"**
    5. Get AI feedback
    6. Click **"Next Question"**
    7. Complete all questions
    """)
    
    st.markdown("---")
    st.caption(f"Role: {get_role_display_name()}")
    st.caption(f"Total Questions: {total_questions}")

# Check if interview is complete
if st.session_state.interview_complete:
    st.success("🎉 **Interview Complete!** Well done!")
    
    st.subheader("📋 Interview Summary")
    
    for i, (q, a, f) in enumerate(zip(
        st.session_state.questions,
        st.session_state.answers,
        st.session_state.feedback
    )):
        with st.expander(f"Question {i+1}: {q[:50]}..."):
            st.write(f"**Your Answer:** {a}")
            st.write(f"**Feedback:** {f}")
    
    if st.button("🔄 Start New Interview"):
        for key in ['current_question_index', 'answers', 'feedback', 
                    'interview_started', 'interview_complete', 'current_answer']:
            if key in st.session_state:
                if key == 'current_question_index':
                    st.session_state[key] = 0
                elif key == 'interview_started':
                    st.session_state[key] = False
                elif key == 'interview_complete':
                    st.session_state[key] = False
                elif key == 'current_answer':
                    st.session_state[key] = ""
                else:
                    st.session_state[key] = []
        st.rerun()

# Start interview
elif not st.session_state.interview_started:
    st.info("👋 Welcome to your AI mock interview!")
    st.write(f"""
    You're about to be interviewed for the **{get_role_display_name()}** role.
    You'll be asked **{len(st.session_state.questions)}** questions.
    
    **Tips:**
    - Take your time to think before answering
    - Be specific and provide examples when possible
    - Don't worry - this is practice!
    """)
    
    if st.button("🚀 Start Interview", type="primary"):
        st.session_state.interview_started = True
        st.rerun()

# Active interview
else:
    current_idx = st.session_state.current_question_index
    total_q = len(st.session_state.questions)
    
    if current_idx >= total_q:
        st.session_state.interview_complete = True
        st.rerun()
    
    current_question = st.session_state.questions[current_idx]
    
    st.subheader(f"Question {current_idx + 1} of {total_q}")
    st.markdown(f"### {current_question}")
    
    # Show previous response
    if len(st.session_state.answers) > 0:
        st.markdown("---")
        st.subheader("📝 Previous Response")
        last_answer = st.session_state.answers[-1]
        last_feedback = st.session_state.feedback[-1] if st.session_state.feedback else "No feedback yet"
        
        st.write(f"**Your Answer:** {last_answer}")
        st.write(f"**Feedback:** {last_feedback}")
    
    st.markdown("---")
    
    # Check if current question already answered
    if current_idx < len(st.session_state.answers):
        st.success("✅ Question answered! Click next to continue.")
        
        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("➡️ Next Question", type="primary"):
                st.session_state.current_question_index += 1
                st.rerun()
    else:
        # Answer input
        answer = st.text_area(
            "✍️ Your Answer:",
            height=150,
            placeholder="Type your answer here...",
            key=f"answer_{current_idx}"
        )
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("📤 Submit Answer", type="primary"):
                if answer.strip():
                    with st.spinner("🤔 Analyzing your answer..."):
                        try:
                            result = run_interview_question(current_question, answer)
                            feedback = result.get("feedback", "Good effort! Keep practicing.")
                            
                            st.session_state.answers.append(answer)
                            st.session_state.feedback.append(feedback)
                            
                            st.success("✅ Answer submitted!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                            st.info("💡 Check your API key in Streamlit Cloud secrets")
                else:
                    st.warning("⚠️ Please type your answer before submitting.")
        
        with col2:
            if st.button("⏭️ Skip Question"):
                st.session_state.answers.append("Skipped")
                st.session_state.feedback.append("No answer provided. It's okay to skip - this is practice!")
                st.session_state.current_question_index += 1
                st.rerun()

# Footer
st.markdown("---")
st.caption("💡 AI Mock Interviewer powered by CrewAI")

# Sidebar status
with st.sidebar:
    st.markdown("---")
    st.header("📊 Status")
    
    if st.session_state.interview_started and not st.session_state.interview_complete:
        st.info(f"**Current Question:** {st.session_state.current_question_index + 1}/{total_q}")
        
        if len(st.session_state.answers) > 0:
            st.success(f"✅ {len(st.session_state.answers)} questions answered")
        else:
            st.warning("⏳ Waiting for first answer")
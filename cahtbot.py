import time
import openai
import streamlit as st
from openai import OpenAIError, RateLimitError

# Set your OpenAI API key
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

# Function to generate technical questions with retries on rate limit error
def generate_questions(tech_stack):
    prompt = f"""
    Generate 3-5 technical interview questions for the following tech stack: {', '.join(tech_stack)}.
    Questions should assess the candidate's proficiency in these technologies.
    """
    
    retries = 3  # Number of retry attempts
    for _ in range(retries):
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": prompt}]
            )
            return response.choices[0].message.content
        except RateLimitError as e:
            st.warning(f"Rate limit exceeded. Retrying... ({_ + 1}/{retries})")
            time.sleep(10)  # Sleep for 10 seconds before retrying
        except OpenAIError as e:
            st.error(f"An error occurred: {e}")
            break  # Exit if any other error occurs
    return None  # Return None if all retries fail

# Initialize Streamlit app
st.title("TalentScout - Hiring Assistant")
st.write("Hello! I'm your Hiring Assistant. Let's start your initial screening.")

# Handle conversation-ending keywords
exit_keywords = ["exit", "quit", "stop"]
user_input = st.text_input("Type 'exit' anytime to leave the chat")
if user_input.lower() in exit_keywords:
    st.write("Thank you for your time! Have a great day!")
    st.stop()

# Collect candidate information
name = st.text_input("Full Name")
email = st.text_input("Email Address")
phone = st.text_input("Phone Number")
experience = st.number_input("Years of Experience", min_value=0, step=1)
position = st.text_input("Desired Position(s)")
location = st.text_input("Current Location")
tech_stack = st.text_area("Enter your tech stack (comma-separated)")

tc_generated = False
if st.button("Submit Details"):
    if name and email and phone and experience and position and location and tech_stack:
        st.subheader("Candidate Details:")
        st.write(f"**Full Name:** {name}")
        st.write(f"**Email:** {email}")
        st.write(f"**Phone Number:** {phone}")
        st.write(f"**Years of Experience:** {experience}")
        st.write(f"**Desired Position(s):** {position}")
        st.write(f"**Current Location:** {location}")
        st.write(f"**Tech Stack:** {tech_stack}")
        st.success("Details submitted successfully!")
    else:
        st.warning("Please fill in all fields before submitting.")

if st.button("Generate Technical Questions"):
    if name and email and phone and experience and position and location and tech_stack:
        tech_list = [tech.strip() for tech in tech_stack.split(',')]
        questions = generate_questions(tech_list)
        if questions:
            st.subheader("Your Technical Questions:")
            st.write(questions)
            tc_generated = True
        else:
            st.error("Failed to generate questions after multiple attempts.")
    else:
        st.warning("Please fill in all fields before generating questions.")

if tc_generated:
    st.write("Thank you for your time! We will reach out to you with the next steps.")
    st.balloons()

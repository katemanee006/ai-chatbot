import streamlit as st
import google.generativeai as genai

st.title("✈️🚄🌏 Travel Planner Chatbot")
st.subheader("Let AI help plan your trip!")

# Capture Gemini API Key
gemini_api_key = st.text_input("Gemini API Key: ", placeholder="Type your API Key here...", type="password")

# Initialize the Gemini Model
if gemini_api_key:
    try:
        # Configure Gemini with the provided API Key
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel("gemini-pro")
        st.success("Gemini API Key successfully configured.")
    except Exception as e:
        st.error(f"An error occurred while setting up the Gemini model: {e}")

# Initialize session state for storing chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # Initialize with an empty list

# Display previous chat history using st.chat_message (if available)
for role, message in st.session_state.chat_history:
    st.chat_message(role).markdown(message)

# Ask user for travel preferences
destination_preference = st.text_input("Where do you want to travel?")
days = st.number_input("How many days is your trip?", min_value=1)

# Replace text input with a checklist for interests
interests = st.multiselect(
    "What are your interests? (Select multiple)",
    options=["Nature", "Food", "Culture", "Adventure", "History", "Shopping", "Relaxation"],
    default=[]
)

# Generate travel plan based on the inputs
if st.button("Create Travel Plan"):
    if model:
        try:
            # Format the selected interests into a string
            interests_str = ", ".join(interests) if interests else "general activities"
            
            # Formulate user input for the travel plan
            user_input = f"Create a {days}-day travel plan for {destination_preference} with interests in {interests_str}."
            
            # Generate response from the model
            response = model.generate_content(user_input)
            bot_response = response.text
            
            # Store and display the bot response
            st.session_state.chat_history.append(("assistant", bot_response))
            st.chat_message("assistant").markdown(bot_response)
        except Exception as e:
            st.error(f"An error occurred while generating the travel plan: {e}")

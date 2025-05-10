import streamlit as st
from openai import OpenAI
import os
import ui
import time
from agents import Agent

# Initialize UI
ui.set_page_config()
ui.load_custom_css()

# Initialize session state variables if they don't exist
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'intake_completed' not in st.session_state:
    st.session_state.intake_completed = False

if 'current_view' not in st.session_state:
    st.session_state.current_view = "input_data"  # Default view

# Initialize empty patient info structure
def initialize_patient_info():
    return {
        "basic": {"name": "", "age": "", "gender": ""},
        "physical": {"height": "", "height_unit": "cm", "weight": "", "weight_unit": "kg"},
        "symptoms": {"primary_complaint": "", "duration": "", "severity": 5, "additional": []},
        "medical_history": {"chronic_conditions": [], "surgeries": ""},
        "medications": {"current_meds": "", "allergies": ""},
        "family_history": {"conditions": ""}
    }

if 'patient_info' not in st.session_state:
    st.session_state.patient_info = initialize_patient_info()

# Initialize OpenAI client in session state
if 'client' not in st.session_state:
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
        if not api_key or api_key == "your-api-key-here":
            st.error("OpenAI API key not found in .streamlit/secrets.toml")
        else:
            st.session_state.client = OpenAI(api_key=api_key)
    except Exception as e:
        st.error(f"Error initializing OpenAI client: {e}")

# Initialize the agent
if 'agent' not in st.session_state:
    try:
        # Create the agent for configuration
        instructions = """You are a virtual doctor assistant. Note that the patient's 
        basic information is already provided to you in the session through an intake form, 
        including their demographics, physical metrics, primary symptoms, medical history, 
        medications, and family history. When the user starts the chat, you should first 
        carefully and thoroughly review ALL of this information to understand the patient's 
        condition before proceeding with the conversation. It is critical that you read and 
        consider every piece of information provided in the intake form, without overlooking 
        any details. 
        
        IMPORTANT: You must ONLY reference information that was explicitly provided in the intake form. 
        DO NOT add, assume, or infer any symptoms, medications, or medical conditions that were not 
        explicitly mentioned in the patient's information. Stick strictly to the facts provided.
        
        You must explicitly tell the patient that you have reviewed their provided information, 
        referencing specific details from their intake form to demonstrate your thorough understanding, 
        and then begin with questions that best match the context of their specific situation. 
        Your main purpose is to analyze this information and ask follow-up questions in a compassionate, 
        structured manner. You utilize a methodical approach of asking one question at a time, 
        carefully listening to each response before proceeding to your next inquiry. This measured 
        pace allows you to thoroughly understand the patient's symptoms, build a comprehensive picture 
        of their health concerns, and ensure they feel heard rather than overwhelmed. 
        
        After gathering sufficient information, you should provide a diagnosis based on the patient's 
        symptoms and medical history, develop an appropriate treatment plan, recommend necessary tests 
        that should be conducted, suggest scheduling an appointment if needed, and determine the best 
        course of action for the patient. Your recommendations should be specific and actionable. 
        
        Throughout your interaction, maintain a professional yet compassionate tone, balancing clinical 
        accuracy with accessible language that addresses both the medical and emotional aspects of the 
        patient's experience."""
        
        st.session_state.agent = Agent(
            name="Virtual Doctor Assistant",
            instructions=instructions,
            model="gpt-4o"
        )
        
        # Initialize the agent's system message
        st.session_state.system_message = {
            "role": "system",
            "content": instructions
        }
        
        # Initialize the agent's conversation history
        st.session_state.agent_messages = [st.session_state.system_message]
    except Exception as e:
        st.error(f"Error creating agent: {e}")

# Common symptoms list for multi-select
COMMON_SYMPTOMS = [
    "Fever", "Cough", "Headache", "Fatigue", "Nausea", "Vomiting", 
    "Diarrhea", "Shortness of breath", "Chest pain", "Back pain",
    "Joint pain", "Rash", "Dizziness", "Sore throat"
]

# Common chronic conditions for multi-select
CHRONIC_CONDITIONS = [
    "Hypertension (High blood pressure)", "Diabetes", "Asthma", 
    "COPD", "Heart disease", "Arthritis", "Depression", "Anxiety",
    "Thyroid disorder", "Kidney disease", "Liver disease"
]

# Function to submit the form
def submit_form():
    st.session_state.intake_completed = True
    
    # Format patient info into a message and add to conversation history
    patient_summary = format_patient_summary()
    
    # Add the patient info as the first message from the assistant to the UI
    st.session_state.messages.append({
        "role": "assistant", 
        "content": f"Thank you for providing your information. I'll be your virtual doctor assistant today. {patient_summary}\n\nHow can I help you today?"
    })
    
    # Add the patient info to the agent context
    if 'agent_messages' in st.session_state:
        try:
            # Add a system message with the patient information
            st.session_state.agent_messages.append({
                "role": "system",
                "content": f"The patient has provided the following information through an intake form: {patient_summary}"
            })
        except Exception as e:
            st.error(f"Error submitting form to agent: {e}")
    
    # Switch to virtual doctor view
    st.session_state.current_view = "virtual_doctor"

# Format patient information into a readable summary
def format_patient_summary():
    p = st.session_state.patient_info
    
    # Basic info
    summary = f"Patient Information:\n"
    summary += f"Name: {p['basic']['name']}\n"
    summary += f"Age: {p['basic']['age']}\n"
    summary += f"Gender: {p['basic']['gender']}\n"
    
    # Physical metrics
    summary += f"Height: {p['physical']['height']} {p['physical']['height_unit']}\n"
    summary += f"Weight: {p['physical']['weight']} {p['physical']['weight_unit']}\n"
    
    # Symptoms
    summary += f"Primary Complaint: {p['symptoms']['primary_complaint']}\n"
    summary += f"Duration: {p['symptoms']['duration']}\n"
    summary += f"Severity (1-10): {p['symptoms']['severity']}\n"
    if p['symptoms']['additional']:
        summary += f"Additional Symptoms: {', '.join(p['symptoms']['additional'])}\n"
    
    # Medical history
    if p['medical_history']['chronic_conditions']:
        summary += f"Chronic Conditions: {', '.join(p['medical_history']['chronic_conditions'])}\n"
    summary += f"Surgeries/Hospitalizations: {p['medical_history']['surgeries']}\n"
    
    # Medications and allergies
    summary += f"Current Medications: {p['medications']['current_meds']}\n"
    summary += f"Allergies: {p['medications']['allergies']}\n"
    
    # Family history
    summary += f"Family History: {p['family_history']['conditions']}\n"
    
    return summary

# Function to call the OpenAI API
def call_openai_api(user_input, model="gpt-4o"):
    try:
        if 'client' not in st.session_state or 'agent_messages' not in st.session_state:
            return "Error: OpenAI client or agent not properly initialized."
        
        # Add the user message to the agent's conversation history
        st.session_state.agent_messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Call the API using the model specified in the agent
        model_to_use = st.session_state.agent.model if hasattr(st.session_state.agent, 'model') and st.session_state.agent.model else model
        
        # Call the API
        response = st.session_state.client.chat.completions.create(
            model=model_to_use,
            messages=st.session_state.agent_messages,
            temperature=0
        )
        
        # Get the assistant's response
        assistant_response = response.choices[0].message.content
        
        # Add the assistant's response to the agent's conversation history
        st.session_state.agent_messages.append({
            "role": "assistant",
            "content": assistant_response
        })
        
        return assistant_response
    
    except Exception as e:
        st.error(f"Error calling OpenAI API: {e}")
        return f"Error: {str(e)}"

# Get model selection, reset button, and current view from sidebar
model_option, reset_button, current_view = ui.render_sidebar()

# Handle reset button
if reset_button:
    # Reset the conversation state
    st.session_state.intake_completed = False
    st.session_state.messages = []
    st.session_state.current_view = "input_data"  # Reset to input data view
    
    # Reset the patient info to empty
    st.session_state.patient_info = initialize_patient_info()
    
    # Reset the agent's conversation history
    if 'system_message' in st.session_state:
        st.session_state.agent_messages = [st.session_state.system_message]
    
    st.rerun()

# Display content based on current view
if current_view == "input_data":
    # Show the intake form
    submit_button = ui.render_intake_form(COMMON_SYMPTOMS, CHRONIC_CONDITIONS)
    
    # Handle form submission
    if submit_button:
        submit_form()
        st.rerun()
        
elif current_view == "virtual_doctor" and st.session_state.intake_completed:
    # Show the chat interface
    ui.render_chat_interface(model_option, call_openai_api)

# Add footer
ui.render_footer()

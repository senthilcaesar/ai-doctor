import streamlit as st
from openai import OpenAI
import os
import ui
import time
import asyncio
import nest_asyncio
import json
import re
from agents import Agent, Runner

# Apply nest_asyncio to allow nested event loops (required for Streamlit)
nest_asyncio.apply()

# Initialize UI
ui.set_page_config()
ui.load_custom_css()

# Function to calculate BMI using Agent and Runner
def calculate_bmi(client, height, weight, height_unit="cm", weight_unit="kg"):
    """
    Calculate BMI and provide health assessment using Agent and Runner.
    
    Args:
        client: OpenAI client instance
        height (float): Height value
        weight (float): Weight value
        height_unit (str): Unit of height ('cm' or 'ft')
        weight_unit (str): Unit of weight ('kg' or 'lb')
        
    Returns:
        dict: BMI information including:
            - bmi_value: The calculated BMI value
            - bmi_category: The BMI category
            - health_assessment: Detailed health assessment
            - recommendations: General health recommendations
    """
    try:
        # Create a BMI calculation agent
        bmi_agent = Agent(
            name="BMI Calculator",
            instructions=f"""You are a BMI calculator. Calculate the BMI for a person with:
            - Height: {height} {height_unit}
            - Weight: {weight} {weight_unit}
            
            1. Convert measurements to metric units if necessary (height in meters, weight in kg)
            2. Calculate BMI using the formula: weight (kg) / (height (m))²
            3. Determine the BMI category (underweight, normal weight, overweight, obese)
            4. Provide a health assessment based on the BMI category
            5. Suggest health recommendations based on the BMI category
            
            Format your response as a JSON object with these keys:
            - bmi_value: The calculated BMI value (rounded to 1 decimal place)
            - bmi_category: The BMI category
            - health_assessment: A brief health assessment
            - recommendations: General health recommendations
            """,
            model="o4-mini-2025-04-16"
        )
        
        # Run the agent
        prompt = f"Calculate BMI for height: {height} {height_unit}, weight: {weight} {weight_unit}"
        result = Runner.run_sync(bmi_agent, prompt)
        
        # Parse the response
        response = result.final_output
        
        try:
            # Try to parse as JSON
            bmi_data = json.loads(response)
            return bmi_data
        except json.JSONDecodeError:
            # If not valid JSON, extract information using regex
            # Extract BMI value
            bmi_value_match = re.search(r'bmi_value"?\s*:?\s*(\d+\.?\d*)', response)
            bmi_value = float(bmi_value_match.group(1)) if bmi_value_match else 0.0
            
            # Extract BMI category
            bmi_category_match = re.search(r'bmi_category"?\s*:?\s*"([^"]+)"', response)
            bmi_category = bmi_category_match.group(1) if bmi_category_match else "Unknown"
            
            # Extract health assessment
            health_assessment_match = re.search(r'health_assessment"?\s*:?\s*"([^"]+)"', response)
            health_assessment = health_assessment_match.group(1) if health_assessment_match else ""
            
            # Extract recommendations
            recommendations_match = re.search(r'recommendations"?\s*:?\s*"([^"]+)"', response)
            recommendations = recommendations_match.group(1) if recommendations_match else ""
            
            return {
                "bmi_value": round(bmi_value, 1),
                "bmi_category": bmi_category,
                "health_assessment": health_assessment,
                "recommendations": recommendations
            }
    except Exception as e:
        # Return a default response in case of error
        return {
            "bmi_value": 0.0,
            "bmi_category": "Error",
            "health_assessment": f"An error occurred while calculating BMI: {str(e)}",
            "recommendations": "Please consult with a healthcare provider for accurate BMI assessment."
        }


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
        "symptoms": {"primary_complaint": "", "duration": "", "severity": 1, "additional": []},
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
        instructions = """
        You are a virtual doctor assistant. Always refer to yourself as 'your virtual doctor assistant' and NEVER use any specific names like 'Dr. Smith' or any other doctor name.

        ## Initial Patient Review
        Before beginning any conversation, carefully and thoroughly review ALL patient information provided through the intake form, including basic information, physical metrics, primary symptoms, medical history, medications, and family history. It is critical that you read and consider every piece of information without overlooking any details. You must ONLY reference information that was explicitly provided - DO NOT add, assume, or infer any symptoms, medications, or medical conditions that were not explicitly mentioned.

        ## Conversation Opening
        After reviewing the patient's information, begin with a warm greeting that acknowledges their specific concern:
        - "Good [morning/afternoon], I'm your virtual doctor assistant. I've reviewed the information you provided about your [primary symptom]. Before we discuss this further, how are you feeling right now?"
        - Explicitly mention that you've reviewed their information, referencing specific details to demonstrate thorough understanding
        - Start with an open-ended question about their main concern

        ## Active Listening and Empathy
        Throughout the conversation:
        - Acknowledge what the patient says before moving to the next question
        - Use empathetic phrases: "I understand," "That must be concerning," "Thank you for sharing that"
        - Reflect back key points: "So you're saying the pain gets worse when..."
        - Express appropriate empathy: "That sounds quite uncomfortable" or "I can see why that would worry you"
        - Ask one question at a time, allowing the patient to fully respond before proceeding
        - Show engagement through natural conversation markers

        ## Clinical Assessment Approach
        When discussing findings or making assessments:
        - Use transitional phrases: "Based on what you've told me..." or "Given your symptoms..."
        - Explain your reasoning: "The reason I'm asking about X is because..."
        - Connect symptoms naturally: "This, combined with your earlier mention of..."
        - Avoid medical jargon unless necessary, and always explain technical terms in simple language
        - Express appropriate uncertainty when warranted: "This could be several things. Let me ask a few more questions to narrow it down..."

        When BMI is relevant to the patient's concern, incorporate it naturally:
        - "I noticed from your measurements that your BMI is [X], which puts you in the [category] range. Given your symptoms of [relevant symptom], this could be playing a role because..."
        - Only emphasize BMI if it's clinically relevant to their presenting concern

        ## Natural Language Guidelines
        Structure conversations to flow naturally:
        - Start with open-ended questions about their main concern
        - Follow up with specific clarifying questions
        - Periodically summarize: "Let me make sure I understand correctly..."
        - Transition smoothly between topics using connecting phrases
        - Use conversational language while maintaining professionalism
        - Adapt your language complexity to match the patient's health literacy level

        Example of natural symptom exploration:
        Patient: "I've been having headaches."
        Assistant: "I'm sorry to hear you're dealing with headaches. Can you tell me how long you've been experiencing them?"
        Patient: "About two weeks."
        Assistant: "Two weeks is quite a while to have headaches. On a scale of 1-10, how would you rate the pain typically?"

        ## Diagnosis and Treatment Planning
        After gathering sufficient information:
        - Provide a clear assessment based on symptoms and medical history
        - Develop specific, actionable treatment recommendations
        - Suggest necessary tests that should be conducted
        - Recommend scheduling appointments when appropriate
        - Always explain the reasoning behind your recommendations
        - Present options when multiple approaches are valid

        ## Cultural Sensitivity and Inclusivity
        - Use inclusive, non-judgmental language
        - Respect privacy and sensitive topics
        - Be mindful of varying health literacy levels
        - Acknowledge when cultural factors might affect care
        - Adapt communication style to patient comfort level

        ## Emergency Recognition
        If the patient describes emergency symptoms (chest pain, severe breathing difficulty, stroke symptoms, etc.):
        - Immediately acknowledge the severity
        - Stay calm but direct
        - Advise: "Based on what you're describing, this needs immediate medical attention. Please call 911 or go to your nearest emergency room right away."
        - Do not attempt to manage emergencies virtually

        ## Conversation Closure
        End conversations naturally and thoroughly:
        - Summarize key points and recommendations
        - Check understanding: "Does this all make sense?" or "Do you have any questions about what we've discussed?"
        - Provide clear, actionable next steps
        - Offer appropriate reassurance when warranted
        - End warmly: "Take care" or "I hope you feel better soon"
        - Remind them when to seek further care if symptoms worsen

        ## Professional Boundaries
        - Maintain professional yet compassionate tone throughout
        - Balance clinical accuracy with accessible language
        - Address both medical and emotional aspects of the patient's experience
        - Never provide definitive diagnoses for serious conditions without proper examination
        - Always recommend in-person care when virtual assessment is insufficient

        IMPORTANT REMINDERS:
        1. Always refer to yourself as 'your virtual doctor assistant' - NEVER use specific names
        2. Only reference information explicitly provided in the intake form
        3. Demonstrate that you've thoroughly reviewed their information in your initial response
        4. Maintain consistent identity and professional boundaries throughout all interactions
        """
        
        # Create the agent using the OpenAI Agents Python library
        st.session_state.agent = Agent(
            name="Virtual Doctor Assistant",
            instructions=instructions,
            model="o4-mini-2025-04-16"
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
    try:
        # Set intake as completed
        st.session_state.intake_completed = True
        
        # Format patient info into a message and add to conversation history
        patient_summary = format_patient_summary()
        
        # Add the patient info as the first message from the assistant to the UI
        if 'messages' not in st.session_state:
            st.session_state.messages = []
            
        # Get patient info for personalized message
        p = st.session_state.patient_info
        
        # Create personalized greeting
        name_greeting = f", {p['basic']['name']}" if p['basic']['name'] else ""
        height_info = f"{p['physical']['height']} {p['physical']['height_unit']}" if p['physical']['height'] else "not provided"
        weight_info = f"{p['physical']['weight']} {p['physical']['weight_unit']}" if p['physical']['weight'] else "not provided"
        symptoms_info = f", as well as your {', '.join(p['symptoms']['additional'])}" if p['symptoms']['additional'] else ""
        conditions_info = f", and note that you have {', '.join(p['medical_history']['chronic_conditions'])}" if p['medical_history']['chronic_conditions'] else ""
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"Thank you for providing your information{name_greeting}. I'll be your virtual doctor assistant today.\n\nWhat brought you here today? I'd like to understand your current health concerns in your own words before we proceed."
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
        
    except Exception as e:
        st.error(f"Error submitting form: {e}")
        # Ensure we still set these values even if there's an error
        st.session_state.intake_completed = True
        st.session_state.current_view = "virtual_doctor"

# Format patient information into a readable summary
def format_patient_summary():
    p = st.session_state.patient_info
    
    # Basic info
    summary = f"Patient Information:\n"
    summary += f"Name: {p['basic']['name'] if p['basic']['name'] else 'Not provided'}\n"
    summary += f"Age: {p['basic']['age'] if p['basic']['age'] else 'Not provided'}\n"
    summary += f"Gender: {p['basic']['gender'] if p['basic']['gender'] else 'Not provided'}\n"
    
    # Physical metrics
    height_str = f"{p['physical']['height']} {p['physical']['height_unit']}" if p['physical']['height'] else 'Not provided'
    weight_str = f"{p['physical']['weight']} {p['physical']['weight_unit']}" if p['physical']['weight'] else 'Not provided'
    summary += f"Height: {height_str}\n"
    summary += f"Weight: {weight_str}\n"
    
    # Calculate BMI if height and weight are provided and are valid numbers
    try:
        if (p['physical']['height'] and p['physical']['weight'] and
            p['physical']['height'].strip() and p['physical']['weight'].strip()):
            try:
                # Try to convert to float
                height_val = float(p['physical']['height'])
                weight_val = float(p['physical']['weight'])
                
                if height_val > 0 and weight_val > 0:
                    bmi_info = calculate_bmi(
                        client=st.session_state.client,
                        height=height_val,
                        weight=weight_val,
                        height_unit=p['physical']['height_unit'],
                        weight_unit=p['physical']['weight_unit']
                    )
                    
                    summary += f"\nBMI Assessment:\n"
                    summary += f"BMI Value: {bmi_info['bmi_value']}\n"
                    summary += f"Category: {bmi_info['bmi_category']}\n"
                    summary += f"Assessment: {bmi_info['health_assessment']}\n"
                    summary += f"Recommendations: {bmi_info['recommendations']}\n"
            except ValueError:
                # If conversion to float fails, skip BMI calculation
                pass
    except Exception as e:
        # Catch any other exceptions that might occur
        pass
    
    # Symptoms
    summary += f"Primary Complaint: {p['symptoms']['primary_complaint'] if p['symptoms']['primary_complaint'] else 'Not provided'}\n"
    summary += f"Duration: {p['symptoms']['duration'] if p['symptoms']['duration'] else 'Not provided'}\n"
    summary += f"Severity (1-10): {p['symptoms']['severity'] if p['symptoms']['severity'] else 'Not provided'}\n"
    if p['symptoms']['additional']:
        summary += f"Additional Symptoms: {', '.join(p['symptoms']['additional'])}\n"
    else:
        summary += "Additional Symptoms: None reported\n"
    
    # Medical history
    if p['medical_history']['chronic_conditions']:
        summary += f"Chronic Conditions: {', '.join(p['medical_history']['chronic_conditions'])}\n"
    else:
        summary += "Chronic Conditions: None reported\n"
        
    summary += f"Surgeries/Hospitalizations: {p['medical_history']['surgeries'] if p['medical_history']['surgeries'] else 'None reported'}\n"
    
    # Medications and allergies
    summary += f"Current Medications: {p['medications']['current_meds'] if p['medications']['current_meds'] else 'None reported'}\n"
    summary += f"Allergies: {p['medications']['allergies'] if p['medications']['allergies'] else 'None reported'}\n"
    
    # Family history
    summary += f"Family History: {p['family_history']['conditions'] if p['family_history']['conditions'] else 'None reported'}\n"
    
    return summary

# Function to call the OpenAI API
def call_openai_api(user_input, model="o4-mini-2025-04-16"):
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
            #temperature=0
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

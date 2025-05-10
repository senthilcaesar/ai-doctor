import streamlit as st
import pandas as pd

# Set page config
def set_page_config():
    st.set_page_config(
        page_title="Virtual Doctor Assistant",
        page_icon="🩺",
        layout="wide",
        initial_sidebar_state="expanded"
    )

# Custom CSS for futuristic sci-fi inspired styling
def load_custom_css():
    st.markdown("""
    <style>
        /* Import fonts */
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700&family=Rajdhani:wght@400;500;700&family=Share+Tech+Mono&display=swap');
        
        /* Theme colors */
        :root {
            --primary-color: #00003c;
            --primary-light: #0000a0;
            --accent-color: #7B42F6;
            --text-color: #333333;
            --bg-primary: #FFFFFF;
            --bg-secondary: #F0F0F0;
            --border-radius: 16px;
            --neon-glow-cyan: 0 0 10px rgba(0, 0, 60, 0.3);
            --neon-glow-magenta: 0 0 10px rgba(255, 0, 228, 0.3);
            --box-shadow: 0 2px 10px -2px rgba(0, 0, 0, 0.05);
        }
        
        /* Typography */
        body {
            font-family: 'Share Tech Mono', sans-serif;
            color: var(--text-color);
        }
        
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Share Tech Mono', sans-serif;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        .neo-data {
            font-family: 'Share Tech Mono', monospace;
            letter-spacing: 0.05em;
        }
        
        /* Layout & Structure */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Sidebar adjustments */
        section[data-testid="stSidebar"] {
            background: var(--bg-secondary);
            border-right: 1px solid #e0e0e0;
            box-shadow: 5px 0 20px rgba(0, 0, 0, 0.5);
        }
        
        /* Badges */
        .neo-badge, .neo-upgrade-badge {
            display: inline-flex;
            align-items: center;
            padding: 0.5rem 1rem;
            font-family: 'Share Tech Mono', monospace;
            font-size: 0.75rem;
            font-weight: 500;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            border-radius: 8px;
        }
        
        .neo-badge {
            background-color: rgba(0, 0, 60, 0.1);
            color: var(--primary-color);
            border: 1px solid var(--primary-color);
            box-shadow: var(--neon-glow-cyan);
        }
        
        .neo-upgrade-badge {
            background-color: rgba(255, 0, 228, 0.1);
            color: var(--primary-light);
            border: 1px solid var(--primary-light);
            box-shadow: var(--neon-glow-magenta);
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            border-bottom: none;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 16px 30px 16px 16px !important;
            border-radius: var(--border-radius) !important;
            background-color: #FFFFFF !important;
            border: 1px solid rgba(0, 0, 60, 0.2) !important;
            font-family: 'Share Tech Mono', monospace !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #87CEEB !important;
            color: var(--primary-color) !important;
            border: 1px solid var(--primary-color) !important;
            box-shadow: var(--neon-glow-cyan) !important;
        }
        
        /* Card styling */
        .neo-card {
            background-color: white;
            border-radius: var(--border-radius);
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            border: 1px solid rgba(0, 0, 60, 0.1);
            box-shadow: var(--box-shadow);
        }
        
        .neo-card-header {
            font-family: 'Share Tech Mono', sans-serif;
            font-size: 1.25rem;
            font-weight: 700;
            margin-bottom: 1rem;
            color: var(--primary-color);
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }
        
        /* Completion indicator */
        .completion-indicator {
            display: inline-flex;
            align-items: center;
            margin-left: 10px;
            font-size: 0.8rem;
        }
        
        .completion-indicator.complete {
            color: #28a745;
        }
        
        .completion-indicator.incomplete {
            color: #dc3545;
        }
        
        /* Required field indicator */
        .required-field::after {
            content: " *";
            color: #dc3545;
            font-weight: bold;
        }
        
        /* Table styling */
        .dataframe {
            width: 100%;
            margin-bottom: 1rem;
            border-collapse: collapse;
        }
        
        .dataframe th {
            background-color: rgba(0, 0, 60, 0.1);
            color: var(--primary-color);
            font-family: 'Share Tech Mono', monospace;
            font-weight: 700;
            text-transform: uppercase;
            padding: 0.75rem;
            border: 1px solid rgba(0, 0, 60, 0.2);
        }
        
        .dataframe td {
            padding: 0.75rem;
            border: 1px solid rgba(0, 0, 60, 0.1);
            font-family: 'Share Tech Mono', monospace;
        }
        
        /* Navigation buttons */
        .nav-button {
            margin-bottom: 10px;
        }
        
        /* Chat styling */
        .stChatMessage {
            padding: 1rem !important;
            margin-bottom: 1rem !important;
            border-radius: var(--border-radius) !important;
        }
        
        .stChatMessage p {
            font-size: 1.1rem !important;
            line-height: 1.5 !important;
        }
        
        .stChatInputContainer {
            padding-top: 1rem !important;
            padding-bottom: 2rem !important;
        }
        
        .stChatInput {
            height: 60px !important;
            font-size: 1.1rem !important;
        }
        
        /* Make chat container taller */
        .chat-container {
            min-height: 600px;
            display: flex;
            flex-direction: column;
        }
        
        .chat-messages {
            flex-grow: 1;
            overflow-y: auto;
            min-height: 500px;
            margin-bottom: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)

# App title and description
def display_header():
    st.markdown("<h1>Virtual Doctor Assistant</h1>", unsafe_allow_html=True)
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <span class="neo-badge">AI-Powered</span>
        <span style="margin-left: 10px;" class="neo-upgrade-badge">Confidential</span>
    </div>
    <p>This application uses OpenAI's API to simulate a virtual doctor that collects patient health information.
    <br><strong>Note:</strong> This app does not provide medical advice or diagnosis.</p>
    """, unsafe_allow_html=True)

# Sidebar for model selection and reset button
def render_sidebar():
    with st.sidebar:
        st.markdown("<div class='neo-card-header'>Virtual Doctor Assistant</div>", unsafe_allow_html=True)
        
        # Initialize current_view in session state if it doesn't exist
        if 'current_view' not in st.session_state:
            st.session_state.current_view = "input_data"  # Default view
        
        # Navigation section
        #st.markdown("### Navigation")
        
        # Input Data button
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown("📋")
        with col2:
            input_data_clicked = st.button(
                "Input Data", 
                use_container_width=True,
                type="primary" if st.session_state.current_view == "input_data" else "secondary",
                key="input_data_button"
            )
        
        # Virtual Doctor button (disabled if intake not completed)
        doctor_button_disabled = not st.session_state.intake_completed
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown("🩺")
        with col2:
            doctor_clicked = st.button(
                "Virtual Doctor", 
                use_container_width=True,
                disabled=doctor_button_disabled,
                type="primary" if st.session_state.current_view == "virtual_doctor" else "secondary",
                key="virtual_doctor_button"
            )
        
        if doctor_button_disabled:
            st.info("Complete and submit the patient information form to enable the Virtual Doctor.")
        
        # Configuration section
        st.markdown("### Configuration")
        model_option = st.selectbox(
            "Select OpenAI model",
            ["o4-mini-2025-04-16", "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
            index=0
        )
        
        #st.info("Using API key from .streamlit/secrets.toml")
        
        # Reset button
        reset_button = st.button("Reset Patient Information", use_container_width=True)
        
        # Handle navigation button clicks
        if input_data_clicked:
            st.session_state.current_view = "input_data"
        if doctor_clicked and not doctor_button_disabled:
            st.session_state.current_view = "virtual_doctor"
        
        return model_option, reset_button, st.session_state.current_view

# Function to check if a tab is complete
def is_tab_complete(tab_name):
    p = st.session_state.patient_info
    
    if tab_name == "Basic Info":
        return p["basic"]["name"] and p["basic"]["age"] > 0
    
    elif tab_name == "Symptoms":
        return p["symptoms"]["primary_complaint"] and p["symptoms"]["duration"]
    
    # Other tabs are optional
    return True

# Function to get completion status for all tabs
def get_tab_completion_status():
    tabs = ["Basic Info", "Physical Metrics", "Symptoms", "Medical History", "Medications", "Family History"]
    return {tab: is_tab_complete(tab) for tab in tabs}

# Function to validate if all required fields are filled
def validate_form_completion():
    # Check if all required tabs are complete
    completion_status = get_tab_completion_status()
    return all(completion_status.values())

# Function to render basic info tab
def render_basic_info(tab):
    tab.markdown("<div class='neo-card-header'>Basic Information</div>", unsafe_allow_html=True)
    
    # Name input
    name = tab.text_input(
        "Full Name", 
        value=st.session_state.patient_info["basic"]["name"],
        help="Enter your full name",
        placeholder="John Doe"
    )
    
    # Age and gender in two columns
    col1, col2 = tab.columns(2)
    
    with col1:
        age = col1.number_input(
            "Age", 
            min_value=0, 
            max_value=120,
            value=int(st.session_state.patient_info["basic"]["age"]) if st.session_state.patient_info["basic"]["age"] else 0,
            help="Enter your age in years"
        )
    
    with col2:
        gender = col2.radio(
            "Gender",
            options=["Male", "Female", "Other"],
            index=["Male", "Female", "Other"].index(st.session_state.patient_info["basic"]["gender"]) if st.session_state.patient_info["basic"]["gender"] in ["Male", "Female", "Other"] else 0,
            horizontal=True
        )
    
    # Show completion status
    if is_tab_complete("Basic Info"):
        tab.success("Basic information complete!")
    
    return name, age, gender

# Function to render physical metrics tab
def render_physical_metrics(tab):
    tab.markdown("<div class='neo-card-header'>Physical Metrics</div>", unsafe_allow_html=True)
    
    # Height with unit selection
    tab.markdown("**Height**")
    col1, col2 = tab.columns([3, 1])
    
    with col1:
        height = col1.number_input(
            "Height Value", 
            min_value=0.0,
            value=float(st.session_state.patient_info["physical"]["height"]) if st.session_state.patient_info["physical"]["height"] else 0.0,
            help="Enter your height"
        )
    
    with col2:
        height_unit = col2.selectbox(
            "Height Unit",
            options=["cm", "ft"],
            index=0 if st.session_state.patient_info["physical"]["height_unit"] == "cm" else 1
        )
    
    # Weight with unit selection
    tab.markdown("**Weight**")
    col1, col2 = tab.columns([3, 1])
    
    with col1:
        weight = col1.number_input(
            "Weight Value",
            min_value=0.0,
            value=float(st.session_state.patient_info["physical"]["weight"]) if st.session_state.patient_info["physical"]["weight"] else 0.0,
            help="Enter your weight"
        )
    
    with col2:
        weight_unit = col2.selectbox(
            "Weight Unit",
            options=["kg", "lb"],
            index=0 if st.session_state.patient_info["physical"]["weight_unit"] == "kg" else 1
        )
    
    # Physical metrics are optional, so always show as complete
    tab.info("Physical metrics are optional but helpful for a complete assessment.")
    
    return height, height_unit, weight, weight_unit

# Function to render symptoms tab
def render_symptoms(tab, COMMON_SYMPTOMS):
    tab.markdown("<div class='neo-card-header'>Current Symptoms</div>", unsafe_allow_html=True)
    
    # Primary complaint
    tab.markdown("**Main Health Concern**")
    primary_complaint = tab.text_area(
        "What is your main health concern today?",
        value=st.session_state.patient_info["symptoms"]["primary_complaint"],
        help="Describe your main symptom or reason for consultation",
        placeholder="Describe your symptoms here..."
    )
    
    # Duration and severity in two columns
    col1, col2 = tab.columns(2)
    
    with col1:
        duration = col1.text_input(
            "How long have you been experiencing this?",
            value=st.session_state.patient_info["symptoms"]["duration"],
            help="e.g., 3 days, 2 weeks, 6 months",
            placeholder="e.g., 3 days"
        )
    
    with col2:
        severity = col2.slider(
            "On a scale of 1-10, how severe is your main concern?",
            min_value=1,
            max_value=10,
            value=st.session_state.patient_info["symptoms"]["severity"],
            help="1 = Very mild, 10 = Extremely severe"
        )
    
    # Additional symptoms multi-select
    tab.markdown("**Additional Symptoms**")
    additional = tab.multiselect(
        "Are you experiencing any other symptoms?",
        options=COMMON_SYMPTOMS,
        default=st.session_state.patient_info["symptoms"]["additional"],
        help="Select all that apply"
    )
    
    # Show completion status
    if is_tab_complete("Symptoms"):
        tab.success("Symptoms information complete!")
    
    return primary_complaint, duration, severity, additional

# Function to render medical history tab
def render_medical_history(tab, CHRONIC_CONDITIONS):
    tab.markdown("<div class='neo-card-header'>Medical History</div>", unsafe_allow_html=True)
    
    # Chronic conditions multi-select
    tab.markdown("**Chronic Medical Conditions**")
    chronic_conditions = tab.multiselect(
        "Do you have any chronic medical conditions?",
        options=CHRONIC_CONDITIONS,
        default=st.session_state.patient_info["medical_history"]["chronic_conditions"],
        help="Select all that apply"
    )
    
    # Previous surgeries/hospitalizations
    tab.markdown("**Previous Surgeries or Hospitalizations**")
    surgeries = tab.text_area(
        "Previous surgeries or hospitalizations",
        value=st.session_state.patient_info["medical_history"]["surgeries"],
        help="Include approximate dates if possible",
        placeholder="e.g., Appendectomy (2018), Hospitalized for pneumonia (2020)"
    )
    
    # Medical history is optional, so always show as complete
    tab.info("Medical history is optional but helpful for a complete assessment.")
    
    return chronic_conditions, surgeries

# Function to render medications tab
def render_medications(tab):
    tab.markdown("<div class='neo-card-header'>Medications & Allergies</div>", unsafe_allow_html=True)
    
    # Current medications
    tab.markdown("**Current Medications**")
    current_meds = tab.text_area(
        "Current medications (including over-the-counter and supplements)",
        value=st.session_state.patient_info["medications"]["current_meds"],
        help="Include dosage if known",
        placeholder="e.g., Lisinopril 10mg daily, Vitamin D 1000 IU daily"
    )
    
    # Allergies
    tab.markdown("**Allergies**")
    allergies = tab.text_area(
        "Allergies to medications or other substances",
        value=st.session_state.patient_info["medications"]["allergies"],
        help="Include your reaction if possible",
        placeholder="e.g., Penicillin (rash), Peanuts (anaphylaxis)"
    )
    
    # Medications are optional, so always show as complete
    tab.info("Medication information is optional but helpful for a complete assessment.")
    
    return current_meds, allergies

# Function to render family history tab
def render_family_history(tab):
    tab.markdown("<div class='neo-card-header'>Family History</div>", unsafe_allow_html=True)
    
    # Family history of conditions
    tab.markdown("**Family History of Medical Conditions**")
    conditions = tab.text_area(
        "Family history of major medical conditions",
        value=st.session_state.patient_info["family_history"]["conditions"],
        help="Include relationship (e.g., 'Mother: diabetes, Father: heart disease')",
        placeholder="e.g., Mother: diabetes, Father: heart disease, Sibling: asthma"
    )
    
    # Family history is optional, so always show as complete
    tab.info("Family history is optional but helpful for a complete assessment.")
    
    return conditions

# Function to create a two-column table from data
def create_two_column_table(data):
    # Create a DataFrame with just the Field and Value columns
    df = pd.DataFrame(data)
    
    # Create HTML for a simple two-column table
    html = "<table style='width:100%; border-collapse: collapse;'>"
    html += "<tr><th style='background-color: rgba(0, 0, 60, 0.1); color: #00003c; padding: 0.75rem; border: 1px solid rgba(0, 0, 60, 0.2);'>Field</th>"
    html += "<th style='background-color: rgba(0, 0, 60, 0.1); color: #00003c; padding: 0.75rem; border: 1px solid rgba(0, 0, 60, 0.2);'>Value</th></tr>"
    
    for i in range(len(df)):
        html += f"<tr><td style='padding: 0.75rem; border: 1px solid rgba(0, 0, 60, 0.1);'>{df['Field'][i]}</td>"
        html += f"<td style='padding: 0.75rem; border: 1px solid rgba(0, 0, 60, 0.1);'>{df['Value'][i]}</td></tr>"
    
    html += "</table>"
    return html

# Function to render submit tab
def render_submit_tab(tab):
    
    # Review summary
    with tab.expander("Click to review your information before submitting", expanded=True):
        p = st.session_state.patient_info
        
        # Basic info
        tab.markdown("<div class='neo-card-header'>Basic Information</div>", unsafe_allow_html=True)
        basic_info_data = {
            "Field": ["Name", "Gender", "Age"],
            "Value": [
                p['basic']['name'] if p['basic']['name'] else 'Not provided',
                p['basic']['gender'] if p['basic']['gender'] else 'Not provided',
                p['basic']['age'] if p['basic']['age'] else 'Not provided'
            ]
        }
        tab.markdown(create_two_column_table(basic_info_data), unsafe_allow_html=True)
        
        # Physical metrics
        tab.markdown("<div class='neo-card-header'>Physical Metrics</div>", unsafe_allow_html=True)
        physical_data = {
            "Field": ["Height", "Weight"],
            "Value": [
                f"{p['physical']['height']} {p['physical']['height_unit']}" if p['physical']['height'] else 'Not provided',
                f"{p['physical']['weight']} {p['physical']['weight_unit']}" if p['physical']['weight'] else 'Not provided'
            ]
        }
        tab.markdown(create_two_column_table(physical_data), unsafe_allow_html=True)
        
        # Symptoms
        tab.markdown("<div class='neo-card-header'>Current Symptoms</div>", unsafe_allow_html=True)
        symptoms_data = {
            "Field": ["Primary Complaint", "Duration", "Severity (1-10)", "Additional Symptoms"],
            "Value": [
                p['symptoms']['primary_complaint'] if p['symptoms']['primary_complaint'] else 'Not provided',
                p['symptoms']['duration'] if p['symptoms']['duration'] else 'Not provided',
                str(p['symptoms']['severity']),
                ', '.join(p['symptoms']['additional']) if p['symptoms']['additional'] else 'None reported'
            ]
        }
        tab.markdown(create_two_column_table(symptoms_data), unsafe_allow_html=True)
        
        # Medical history
        if p['medical_history']['chronic_conditions'] or p['medical_history']['surgeries']:
            tab.markdown("<div class='neo-card-header'>Medical History</div>", unsafe_allow_html=True)
            medical_data = {
                "Field": [],
                "Value": []
            }
            if p['medical_history']['chronic_conditions']:
                medical_data["Field"].append("Chronic Conditions")
                medical_data["Value"].append(', '.join(p['medical_history']['chronic_conditions']))
            if p['medical_history']['surgeries']:
                medical_data["Field"].append("Surgeries/Hospitalizations")
                medical_data["Value"].append(p['medical_history']['surgeries'])
            
            tab.markdown(create_two_column_table(medical_data), unsafe_allow_html=True)
        
        # Medications and allergies
        if p['medications']['current_meds'] or p['medications']['allergies']:
            tab.markdown("<div class='neo-card-header'>Medications & Allergies</div>", unsafe_allow_html=True)
            meds_data = {
                "Field": [],
                "Value": []
            }
            if p['medications']['current_meds']:
                meds_data["Field"].append("Current Medications")
                meds_data["Value"].append(p['medications']['current_meds'])
            if p['medications']['allergies']:
                meds_data["Field"].append("Allergies")
                meds_data["Value"].append(p['medications']['allergies'])
            
            tab.markdown(create_two_column_table(meds_data), unsafe_allow_html=True)
        
        # Family history
        if p['family_history']['conditions']:
            tab.markdown("<div class='neo-card-header'>Family History</div>", unsafe_allow_html=True)
            family_data = {
                "Field": ["Family History"],
                "Value": [p['family_history']['conditions']]
            }
            tab.markdown(create_two_column_table(family_data), unsafe_allow_html=True)
    
    # Submit button
    tab.markdown("### Submit Your Information")
    
    # Check if all required fields are complete
    form_complete = validate_form_completion()
    if not form_complete:
        tab.warning("Please complete all required fields in the Basic Info and Symptoms tabs before submitting.")
    else:
        tab.success("All required information has been provided. You can now submit the form.")
    
    submit_button = tab.button("Submit Information", type="primary", use_container_width=True)
    
    return submit_button

# Function to render the intake form
def render_intake_form(COMMON_SYMPTOMS, CHRONIC_CONDITIONS):
    st.markdown("<div class='neo-card-header'>Patient Information Intake Form</div>", unsafe_allow_html=True)
    
    # Create tabs for different sections of the form
    tabs = st.tabs(["Basic Info", "Physical Metrics", "Symptoms", "Medical History", "Medications", "Family History", "Submit Information"])
    
    # Initialize submit_button to False
    submit_button = False
    
    # Render each tab and collect the input values
    with tabs[0]:
        name, age, gender = render_basic_info(tabs[0])
        st.session_state.patient_info["basic"]["name"] = name
        st.session_state.patient_info["basic"]["age"] = age
        st.session_state.patient_info["basic"]["gender"] = gender
    
    with tabs[1]:
        height, height_unit, weight, weight_unit = render_physical_metrics(tabs[1])
        st.session_state.patient_info["physical"]["height"] = height
        st.session_state.patient_info["physical"]["height_unit"] = height_unit
        st.session_state.patient_info["physical"]["weight"] = weight
        st.session_state.patient_info["physical"]["weight_unit"] = weight_unit
    
    with tabs[2]:
        primary_complaint, duration, severity, additional = render_symptoms(tabs[2], COMMON_SYMPTOMS)
        st.session_state.patient_info["symptoms"]["primary_complaint"] = primary_complaint
        st.session_state.patient_info["symptoms"]["duration"] = duration
        st.session_state.patient_info["symptoms"]["severity"] = severity
        st.session_state.patient_info["symptoms"]["additional"] = additional
    
    with tabs[3]:
        chronic_conditions, surgeries = render_medical_history(tabs[3], CHRONIC_CONDITIONS)
        st.session_state.patient_info["medical_history"]["chronic_conditions"] = chronic_conditions
        st.session_state.patient_info["medical_history"]["surgeries"] = surgeries
    
    with tabs[4]:
        current_meds, allergies = render_medications(tabs[4])
        st.session_state.patient_info["medications"]["current_meds"] = current_meds
        st.session_state.patient_info["medications"]["allergies"] = allergies
    
    with tabs[5]:
        conditions = render_family_history(tabs[5])
        st.session_state.patient_info["family_history"]["conditions"] = conditions
    
    with tabs[6]:
        submit_button = render_submit_tab(tabs[6])
    
    return submit_button

# Function to render the chat interface
def render_chat_interface(model_option, call_openai_api):
    # Display conversation history
    st.markdown("<div class='neo-card-header'>Conversation with Virtual Doctor</div>", unsafe_allow_html=True)
    
    # Create a container for the chat with increased height
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    
    # Create a container for the messages with scrolling
    st.markdown("<div class='chat-messages'>", unsafe_allow_html=True)
    
    # Display conversation history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    st.markdown("</div>", unsafe_allow_html=True)  # Close chat-messages div
    
    # User input area - make it larger
    user_input = st.chat_input("Type your message here...", key="chat_input")
    
    st.markdown("</div>", unsafe_allow_html=True)  # Close chat-container div
    
    # Process user input and generate response
    if user_input:
        # Display user message
        with st.chat_message("user"):
            st.write(user_input)
        
        # Add user message to conversation history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Show a spinner while waiting for the API response
        with st.spinner("Virtual doctor is thinking..."):
            response = call_openai_api(user_input, model_option)
        
        # Display assistant response
        with st.chat_message("assistant"):
            st.write(response)
        
        # Add assistant response to conversation history
        st.session_state.messages.append({"role": "assistant", "content": response})

# Function to render the footer
def render_footer():
    st.markdown("---")
    st.markdown("<div style='text-align: center; color: #888;'>Virtual Doctor Assistant | For demonstration purposes only</div>", unsafe_allow_html=True)

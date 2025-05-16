import streamlit as st
from bayesian_engine import BayesianDiagnosisEngine
import re

class BayesianDoctorIntegration:
    """
    Integration class that connects the Bayesian diagnosis engine with the doctor agent.
    This class handles the extraction of symptoms from conversations, updating the Bayesian
    engine, and enhancing the doctor agent's responses with Bayesian reasoning.
    """
    
    def __init__(self):
        """Initialize the Bayesian doctor integration."""
        # Initialize the Bayesian diagnosis engine
        self.engine = BayesianDiagnosisEngine()
        
        # Initialize session state for Bayesian engine if not already present
        if 'bayesian_engine_state' not in st.session_state:
            st.session_state.bayesian_engine_state = {
                'observed_symptoms': {},  # Symptoms observed so far
                'current_beliefs': self.engine.beliefs.copy(),  # Current belief state
                'diagnosis_history': [],  # History of diagnoses
                'suggested_questions': []  # Suggested questions to ask
            }
    
    def extract_symptoms_from_text(self, text):
        """
        Extract symptoms from text using pattern matching.
        
        Args:
            text (str): The text to extract symptoms from
        
        Returns:
            dict: Dictionary of symptoms and their values (True for present, False for absent)
        """
        # Convert text to lowercase for case-insensitive matching
        text_lower = text.lower()
        
        # Dictionary to store extracted symptoms
        extracted_symptoms = {}
        
        # Check for each symptom in the knowledge base
        for symptom in self.engine.symptom_given_disease:
            # Create patterns for positive and negative mentions of the symptom
            symptom_lower = symptom.lower()
            
            # Positive patterns (symptom is present)
            positive_patterns = [
                rf"(?:i|patient)(?:'s| is| am| have| has| having| experiencing| feeling| suffering from| with) (?:a |an |the )?{symptom_lower}",
                rf"{symptom_lower}(?:^|$| )",
                rf"(?:having|have|has|experiencing|with) (?:a |an |the )?{symptom_lower}",
                rf"(?:complaining of|reports|reported|mentions|mentioned) (?:a |an |the )?{symptom_lower}",
                rf"(?:positive for|confirmed) (?:a |an |the )?{symptom_lower}"
            ]
            
            # Negative patterns (symptom is absent)
            negative_patterns = [
                rf"(?:no|not|doesn't|don't|does not|do not|without|denies|denied) (?:a |an |the )?{symptom_lower}",
                rf"(?:no|not|doesn't|don't|does not|do not|without|denies|denied) (?:having|have|has|experiencing) (?:a |an |the )?{symptom_lower}",
                rf"(?:negative for) (?:a |an |the )?{symptom_lower}"
            ]
            
            # Check for positive mentions
            is_positive = any(re.search(pattern, text_lower) for pattern in positive_patterns)
            
            # Check for negative mentions
            is_negative = any(re.search(pattern, text_lower) for pattern in negative_patterns)
            
            # If there's a clear positive or negative mention, record it
            if is_positive and not is_negative:
                extracted_symptoms[symptom] = True
            elif is_negative and not is_positive:
                extracted_symptoms[symptom] = False
        
        return extracted_symptoms
    
    def extract_symptoms_from_intake(self, patient_info):
        """
        Extract symptoms from patient intake information.
        
        Args:
            patient_info (dict): Patient information from intake form
        
        Returns:
            dict: Dictionary of symptoms and their values (True for present, False for absent)
        """
        extracted_symptoms = {}
        
        # Extract primary complaint
        if patient_info.get('symptoms', {}).get('primary_complaint'):
            primary_complaint = patient_info['symptoms']['primary_complaint']
            # Extract symptoms from primary complaint
            complaint_symptoms = self.extract_symptoms_from_text(primary_complaint)
            extracted_symptoms.update(complaint_symptoms)
        
        # Extract additional symptoms
        if patient_info.get('symptoms', {}).get('additional'):
            for symptom in patient_info['symptoms']['additional']:
                # Check if the symptom is in our knowledge base
                for known_symptom in self.engine.symptom_given_disease:
                    if symptom.lower() in known_symptom.lower() or known_symptom.lower() in symptom.lower():
                        extracted_symptoms[known_symptom] = True
                        break
        
        return extracted_symptoms
    
    def update_from_conversation(self, user_input, assistant_response):
        """
        Update the Bayesian engine based on the conversation.
        
        Args:
            user_input (str): The user's input message
            assistant_response (str): The assistant's response
        
        Returns:
            dict: Updated belief state
        """
        # Extract symptoms from user input
        user_symptoms = self.extract_symptoms_from_text(user_input)
        
        # Extract symptoms from assistant response (might contain confirmations)
        assistant_symptoms = self.extract_symptoms_from_text(assistant_response)
        
        # Combine symptoms, giving priority to user input
        all_symptoms = {**assistant_symptoms, **user_symptoms}
        
        # Update the Bayesian engine with each symptom
        for symptom, has_symptom in all_symptoms.items():
            # Only update if this is a new observation or different from previous observation
            if symptom not in st.session_state.bayesian_engine_state['observed_symptoms'] or \
               st.session_state.bayesian_engine_state['observed_symptoms'][symptom] != has_symptom:
                self.engine.update_belief(symptom, has_symptom)
                # Record the observation
                st.session_state.bayesian_engine_state['observed_symptoms'][symptom] = has_symptom
        
        # Update current beliefs in session state
        st.session_state.bayesian_engine_state['current_beliefs'] = self.engine.beliefs.copy()
        
        # Get top diagnoses
        top_diagnoses = self.engine.get_top_diagnoses(3)
        
        # Add to diagnosis history if different from last diagnosis
        if not st.session_state.bayesian_engine_state['diagnosis_history'] or \
           st.session_state.bayesian_engine_state['diagnosis_history'][-1][0][0] != top_diagnoses[0][0]:
            st.session_state.bayesian_engine_state['diagnosis_history'].append(top_diagnoses)
        
        # Update suggested questions
        st.session_state.bayesian_engine_state['suggested_questions'] = self.engine.suggest_questions(3)
        
        return self.engine.beliefs
    
    def update_from_intake(self, patient_info):
        """
        Update the Bayesian engine based on patient intake information.
        
        Args:
            patient_info (dict): Patient information from intake form
        
        Returns:
            dict: Updated belief state
        """
        # Extract symptoms from intake information
        intake_symptoms = self.extract_symptoms_from_intake(patient_info)
        
        # Reset the engine to start fresh
        self.engine.reset()
        st.session_state.bayesian_engine_state['observed_symptoms'] = {}
        
        # Update the Bayesian engine with each symptom
        for symptom, has_symptom in intake_symptoms.items():
            self.engine.update_belief(symptom, has_symptom)
            # Record the observation
            st.session_state.bayesian_engine_state['observed_symptoms'][symptom] = has_symptom
        
        # Update current beliefs in session state
        st.session_state.bayesian_engine_state['current_beliefs'] = self.engine.beliefs.copy()
        
        # Get top diagnoses
        top_diagnoses = self.engine.get_top_diagnoses(3)
        
        # Initialize diagnosis history
        st.session_state.bayesian_engine_state['diagnosis_history'] = [top_diagnoses]
        
        # Update suggested questions
        st.session_state.bayesian_engine_state['suggested_questions'] = self.engine.suggest_questions(3)
        
        return self.engine.beliefs
    
    def get_diagnostic_summary(self):
        """
        Get a summary of the current diagnostic state.
        
        Returns:
            str: Diagnostic summary
        """
        # Get top diagnoses
        top_diagnoses = self.engine.get_top_diagnoses(3)
        
        # Format the diagnostic summary
        summary = "## Bayesian Diagnostic Assessment\n\n"
        
        # Add top diagnoses
        summary += "### Top Differential Diagnoses\n"
        for i, (disease, probability) in enumerate(top_diagnoses, 1):
            confidence_level = "High" if probability > 0.7 else "Moderate" if probability > 0.4 else "Low"
            summary += f"{i}. **{disease}** (Probability: {probability:.2f}, Confidence: {confidence_level})\n"
        
        # Add observed symptoms
        if st.session_state.bayesian_engine_state['observed_symptoms']:
            summary += "\n### Observed Symptoms\n"
            for symptom, has_symptom in st.session_state.bayesian_engine_state['observed_symptoms'].items():
                status = "Present" if has_symptom else "Absent"
                summary += f"- {symptom}: {status}\n"
        
        # Add suggested questions
        if st.session_state.bayesian_engine_state['suggested_questions']:
            summary += "\n### Suggested Follow-up Questions\n"
            for symptom, info_gain in st.session_state.bayesian_engine_state['suggested_questions']:
                summary += f"- Ask about {symptom} (Information Gain: {info_gain:.3f})\n"
        
        return summary
    
    def get_detailed_diagnosis(self, disease=None):
        """
        Get a detailed explanation of a specific diagnosis.
        
        Args:
            disease (str, optional): The disease to explain. If None, explains the top diagnosis.
        
        Returns:
            str: Detailed diagnosis explanation
        """
        # If no disease specified, use the top diagnosis
        if disease is None:
            top_diagnoses = self.engine.get_top_diagnoses(1)
            if not top_diagnoses:
                return "No diagnosis available."
            disease = top_diagnoses[0][0]
        
        # Get the explanation
        explanation = self.engine.explain_reasoning(disease)
        
        # Format the detailed diagnosis
        detail = f"## Detailed Analysis: {disease}\n\n"
        detail += f"{explanation['explanation']}\n\n"
        
        # Add supporting evidence
        if explanation['evidence_factors']:
            detail += "### Evidence Factors\n"
            for factor in explanation['evidence_factors']:
                symptom_status = "Presence" if factor['present'] else "Absence"
                effect = factor['effect'].capitalize()
                strength = factor['strength'].capitalize()
                detail += f"- {symptom_status} of {factor['symptom']}: {strength} {effect} factor "
                detail += f"(Likelihood: {factor['likelihood_factor']:.2f})\n"
        
        return detail
    
    def enhance_response(self, user_input, assistant_response):
        """
        Update the Bayesian engine based on the conversation but keep the diagnostic
        assessment internal to the agent.
        
        Args:
            user_input (str): The user's input message
            assistant_response (str): The assistant's response
        
        Returns:
            str: The original assistant response (no Bayesian information added)
        """
        # Update the Bayesian engine based on the conversation
        self.update_from_conversation(user_input, assistant_response)
        
        # Get the diagnostic summary and detailed diagnosis for internal use only
        # This information is not added to the response but can be used by the agent
        # to guide its reasoning and question selection
        diagnostic_summary = self.get_diagnostic_summary()
        
        # Get the top diagnoses
        top_diagnoses = self.engine.get_top_diagnoses(3)
        
        # Get suggested questions for internal use
        suggested_questions = self.engine.suggest_questions(3)
        
        # Log the diagnostic information for debugging (not visible to the user)
        if st.session_state.bayesian_engine_state['observed_symptoms']:
            print("\nBayesian Diagnostic Assessment (Internal):")
            print(f"Top diagnoses: {top_diagnoses}")
            print(f"Suggested questions: {suggested_questions}")
        
        # Return the original response without adding Bayesian information
        return assistant_response
    
    def get_next_question(self):
        """
        Get the next question to ask based on information gain.
        
        Returns:
            str: Next question to ask
        """
        # Get suggested questions
        suggested_questions = st.session_state.bayesian_engine_state.get('suggested_questions', [])
        
        if not suggested_questions:
            return "Could you tell me more about your symptoms?"
        
        # Get the top suggested question
        top_symptom, _ = suggested_questions[0]
        
        # Format the question based on the symptom
        question_templates = {
            "Fever": "Have you been experiencing any fever?",
            "Cough": "Do you have a cough?",
            "Shortness of Breath": "Have you noticed any difficulty breathing or shortness of breath?",
            "Fatigue": "Have you been feeling unusually tired or fatigued?",
            "Headache": "Have you been having headaches?",
            "Sore Throat": "Do you have a sore throat?",
            "Runny Nose": "Do you have a runny nose?",
            "Nasal Congestion": "Are you experiencing nasal congestion or a stuffy nose?",
            "Sneezing": "Have you been sneezing more than usual?",
            "Chest Pain": "Have you experienced any chest pain or discomfort?",
            "Wheezing": "Have you noticed any wheezing or whistling sound when breathing?",
            "Nausea": "Have you felt nauseous?",
            "Vomiting": "Have you had any vomiting?",
            "Diarrhea": "Have you experienced diarrhea?",
            "Abdominal Pain": "Have you had any abdominal pain or discomfort?",
            "Muscle Aches": "Are you experiencing any muscle aches or pains?",
            "Joint Pain": "Do you have any joint pain?",
            "Chills": "Have you had chills or felt unusually cold?",
            "Loss of Taste/Smell": "Have you noticed any changes in your sense of taste or smell?",
            "Itchy Eyes": "Are your eyes itchy?",
            "Ear Pain": "Have you experienced any ear pain?",
            "Frequent Urination": "Have you been urinating more frequently than usual?",
            "Painful Urination": "Do you experience pain or burning when urinating?",
            "Blood in Urine": "Have you noticed any blood in your urine?",
            "Heartburn": "Do you experience heartburn or a burning sensation in your chest?",
            "Regurgitation": "Have you experienced regurgitation or food coming back up after eating?",
            "Light Sensitivity": "Are you sensitive to light?",
            "Sound Sensitivity": "Are you sensitive to sound?"
        }
        
        # Get the question for the top symptom
        question = question_templates.get(top_symptom, f"Do you have {top_symptom.lower()}?")
        
        return question
    
    def reset(self):
        """Reset the Bayesian engine and session state."""
        self.engine.reset()
        st.session_state.bayesian_engine_state = {
            'observed_symptoms': {},
            'current_beliefs': self.engine.beliefs.copy(),
            'diagnosis_history': [],
            'suggested_questions': []
        }

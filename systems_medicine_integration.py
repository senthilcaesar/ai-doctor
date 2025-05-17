import streamlit as st
from systems_medicine import SystemsMedicineModel
from bayesian_engine import BayesianDiagnosisEngine
import re

class SystemsMedicineIntegration:
    """
    Integration class that connects the Systems Medicine model with the Bayesian diagnosis engine
    and doctor agent. This class provides a unified approach to healthcare by considering the
    interconnections between different body systems and analyzing symptoms across medical specialties.
    """
    
    def __init__(self, bayesian_integration=None):
        """
        Initialize the Systems Medicine integration.
        
        Args:
            bayesian_integration: Optional BayesianDoctorIntegration instance to connect with
        """
        # Initialize the Systems Medicine model
        self.model = SystemsMedicineModel()
        
        # Store reference to Bayesian integration if provided
        self.bayesian_integration = bayesian_integration
        
        # Initialize session state for Systems Medicine if not already present
        if 'systems_medicine_state' not in st.session_state:
            st.session_state.systems_medicine_state = {
                'reported_symptoms': [],  # Symptoms reported by the patient
                'asked_symptoms': [],     # Symptoms already asked about
                'affected_systems': {},   # Systems affected based on symptoms
                'lifestyle_factors': {},  # Lifestyle factors mentioned
                'suggested_questions': [] # Suggested questions to ask
            }
    
    def extract_symptoms_from_text(self, text):
        """
        Extract symptoms from text using pattern matching.
        
        Args:
            text (str): The text to extract symptoms from
        
        Returns:
            list: List of symptoms mentioned in the text
        """
        # Convert text to lowercase for case-insensitive matching
        text_lower = text.lower()
        
        # List to store extracted symptoms
        extracted_symptoms = []
        
        # Check for each symptom in the knowledge base
        for symptom in self.model.symptom_system_mapping:
            # Create patterns for positive mentions of the symptom
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
            
            # If there's a clear positive mention and not a negative mention, add to extracted symptoms
            if is_positive and not is_negative:
                extracted_symptoms.append(symptom)
        
        return extracted_symptoms
    
    def extract_lifestyle_factors_from_text(self, text):
        """
        Extract lifestyle factors from text.
        
        Args:
            text (str): The text to extract lifestyle factors from
        
        Returns:
            dict: Dictionary of lifestyle factors and their mentions
        """
        # Convert text to lowercase for case-insensitive matching
        text_lower = text.lower()
        
        # Dictionary to store extracted lifestyle factors
        extracted_factors = {}
        
        # Define lifestyle factors to look for
        lifestyle_factors = {
            "Diet": ["diet", "food", "eating", "nutrition", "meal", "vegetarian", "vegan", "gluten", "dairy", "sugar", "carb"],
            "Sleep": ["sleep", "insomnia", "rest", "tired", "fatigue", "nap", "bedtime", "waking up"],
            "Exercise": ["exercise", "workout", "physical activity", "sedentary", "walking", "running", "gym", "sports"],
            "Stress": ["stress", "anxiety", "worried", "tension", "relaxation", "meditation", "mindfulness", "work-life balance"],
            "Environmental": ["pollution", "allergen", "toxin", "chemical", "air quality", "water quality", "mold", "environment"]
        }
        
        # Check for mentions of each lifestyle factor
        for factor, keywords in lifestyle_factors.items():
            for keyword in keywords:
                if keyword in text_lower:
                    if factor not in extracted_factors:
                        extracted_factors[factor] = []
                    extracted_factors[factor].append(keyword)
        
        return extracted_factors
    
    def extract_from_intake(self, patient_info):
        """
        Extract symptoms and lifestyle factors from patient intake information.
        
        Args:
            patient_info (dict): Patient information from intake form
        
        Returns:
            tuple: (extracted_symptoms, extracted_lifestyle_factors)
        """
        extracted_symptoms = []
        extracted_lifestyle = {}
        
        # Extract from primary complaint
        if patient_info.get('symptoms', {}).get('primary_complaint'):
            primary_complaint = patient_info['symptoms']['primary_complaint']
            # Extract symptoms from primary complaint
            complaint_symptoms = self.extract_symptoms_from_text(primary_complaint)
            extracted_symptoms.extend(complaint_symptoms)
            
            # Extract lifestyle factors from primary complaint
            lifestyle_factors = self.extract_lifestyle_factors_from_text(primary_complaint)
            for factor, mentions in lifestyle_factors.items():
                if factor not in extracted_lifestyle:
                    extracted_lifestyle[factor] = []
                extracted_lifestyle[factor].extend(mentions)
        
        # Extract from additional symptoms
        if patient_info.get('symptoms', {}).get('additional'):
            for symptom in patient_info['symptoms']['additional']:
                # Check if the symptom is in our knowledge base
                for known_symptom in self.model.symptom_system_mapping:
                    if symptom.lower() in known_symptom.lower() or known_symptom.lower() in symptom.lower():
                        if known_symptom not in extracted_symptoms:
                            extracted_symptoms.append(known_symptom)
                        break
        
        # Extract from medical history
        if patient_info.get('medical_history', {}).get('surgeries'):
            surgeries = patient_info['medical_history']['surgeries']
            # Extract symptoms from surgeries
            surgery_symptoms = self.extract_symptoms_from_text(surgeries)
            extracted_symptoms.extend([s for s in surgery_symptoms if s not in extracted_symptoms])
            
            # Extract lifestyle factors from surgeries
            lifestyle_factors = self.extract_lifestyle_factors_from_text(surgeries)
            for factor, mentions in lifestyle_factors.items():
                if factor not in extracted_lifestyle:
                    extracted_lifestyle[factor] = []
                extracted_lifestyle[factor].extend(mentions)
        
        # Extract from medications
        if patient_info.get('medications', {}).get('current_meds'):
            medications = patient_info['medications']['current_meds']
            # Extract lifestyle factors from medications
            lifestyle_factors = self.extract_lifestyle_factors_from_text(medications)
            for factor, mentions in lifestyle_factors.items():
                if factor not in extracted_lifestyle:
                    extracted_lifestyle[factor] = []
                extracted_lifestyle[factor].extend(mentions)
        
        # Extract from family history
        if patient_info.get('family_history', {}).get('conditions'):
            family_history = patient_info['family_history']['conditions']
            # Extract lifestyle factors from family history
            lifestyle_factors = self.extract_lifestyle_factors_from_text(family_history)
            for factor, mentions in lifestyle_factors.items():
                if factor not in extracted_lifestyle:
                    extracted_lifestyle[factor] = []
                extracted_lifestyle[factor].extend(mentions)
        
        return extracted_symptoms, extracted_lifestyle
    
    def update_from_conversation(self, user_input, assistant_response):
        """
        Update the Systems Medicine model based on the conversation.
        
        Args:
            user_input (str): The user's input message
            assistant_response (str): The assistant's response
        
        Returns:
            dict: Updated state
        """
        # Extract symptoms from user input
        user_symptoms = self.extract_symptoms_from_text(user_input)
        
        # Extract symptoms from assistant response (might contain confirmations)
        assistant_symptoms = self.extract_symptoms_from_text(assistant_response)
        
        # Combine symptoms
        all_symptoms = list(set(user_symptoms + assistant_symptoms))
        
        # Extract lifestyle factors from user input
        user_lifestyle = self.extract_lifestyle_factors_from_text(user_input)
        
        # Extract lifestyle factors from assistant response
        assistant_lifestyle = self.extract_lifestyle_factors_from_text(assistant_response)
        
        # Combine lifestyle factors
        all_lifestyle = {}
        for factor in set(list(user_lifestyle.keys()) + list(assistant_lifestyle.keys())):
            all_lifestyle[factor] = list(set(user_lifestyle.get(factor, []) + assistant_lifestyle.get(factor, [])))
        
        # Update reported symptoms in session state
        for symptom in all_symptoms:
            if symptom not in st.session_state.systems_medicine_state['reported_symptoms']:
                st.session_state.systems_medicine_state['reported_symptoms'].append(symptom)
        
        # Update lifestyle factors in session state
        for factor, mentions in all_lifestyle.items():
            if factor not in st.session_state.systems_medicine_state['lifestyle_factors']:
                st.session_state.systems_medicine_state['lifestyle_factors'][factor] = []
            st.session_state.systems_medicine_state['lifestyle_factors'][factor].extend(mentions)
        
        # Analyze affected systems based on reported symptoms
        st.session_state.systems_medicine_state['affected_systems'] = self.model.analyze_symptom_pattern(
            st.session_state.systems_medicine_state['reported_symptoms']
        )
        
        # Update suggested questions
        st.session_state.systems_medicine_state['suggested_questions'] = self.model.suggest_related_questions(
            st.session_state.systems_medicine_state['reported_symptoms'],
            st.session_state.systems_medicine_state['asked_symptoms']
        )
        
        # If a question about a symptom was asked, add it to asked_symptoms
        for symptom in self.model.symptom_system_mapping:
            symptom_lower = symptom.lower()
            question_patterns = [
                rf"(?:do you have|are you experiencing|have you noticed|have you had) (?:a |an |the |any )?{symptom_lower}",
                rf"(?:have you been having|have you been experiencing) (?:a |an |the |any )?{symptom_lower}",
                rf"(?:tell me about|what about) (?:your |any )?{symptom_lower}"
            ]
            
            if any(re.search(pattern, assistant_response.lower()) for pattern in question_patterns):
                if symptom not in st.session_state.systems_medicine_state['asked_symptoms']:
                    st.session_state.systems_medicine_state['asked_symptoms'].append(symptom)
        
        return st.session_state.systems_medicine_state
    
    def update_from_intake(self, patient_info):
        """
        Update the Systems Medicine model based on patient intake information.
        
        Args:
            patient_info (dict): Patient information from intake form
        
        Returns:
            dict: Updated state
        """
        # Extract symptoms and lifestyle factors from intake
        intake_symptoms, intake_lifestyle = self.extract_from_intake(patient_info)
        
        # Reset the state
        st.session_state.systems_medicine_state = {
            'reported_symptoms': [],
            'asked_symptoms': [],
            'affected_systems': {},
            'lifestyle_factors': {},
            'suggested_questions': []
        }
        
        # Update reported symptoms
        st.session_state.systems_medicine_state['reported_symptoms'] = intake_symptoms
        
        # Update lifestyle factors
        st.session_state.systems_medicine_state['lifestyle_factors'] = intake_lifestyle
        
        # Analyze affected systems
        st.session_state.systems_medicine_state['affected_systems'] = self.model.analyze_symptom_pattern(intake_symptoms)
        
        # Update suggested questions
        st.session_state.systems_medicine_state['suggested_questions'] = self.model.suggest_related_questions(
            intake_symptoms,
            []  # No asked symptoms yet
        )
        
        return st.session_state.systems_medicine_state
    
    def get_holistic_assessment(self):
        """
        Get a holistic assessment based on the current state.
        
        Returns:
            dict: Holistic assessment
        """
        # Generate holistic assessment
        assessment = self.model.generate_holistic_assessment(
            st.session_state.systems_medicine_state['reported_symptoms'],
            st.session_state.systems_medicine_state['lifestyle_factors']
        )
        
        return assessment
    
    def get_cross_specialty_insights(self):
        """
        Get insights that span multiple medical specialties.
        
        Returns:
            dict: Cross-specialty insights
        """
        if not st.session_state.systems_medicine_state['reported_symptoms']:
            return {"insights": "No symptoms reported to analyze."}
        
        # Get affected systems
        affected_systems = st.session_state.systems_medicine_state['affected_systems']
        top_systems = sorted(affected_systems.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # Map systems to medical specialties
        system_to_specialty = {
            "Neurological": "Neurology",
            "Endocrine": "Endocrinology",
            "Immune": "Immunology",
            "Digestive": "Gastroenterology",
            "Cardiovascular": "Cardiology",
            "Respiratory": "Pulmonology",
            "Musculoskeletal": "Orthopedics/Rheumatology",
            "Integumentary": "Dermatology",
            "Urinary": "Urology/Nephrology",
            "Reproductive": "Gynecology/Urology",
            "Mental Health": "Psychiatry/Psychology",
            "Metabolic": "Endocrinology/Nutrition"
        }
        
        # Get specialties involved
        specialties_involved = [(system_to_specialty.get(system, system), score) for system, score in top_systems]
        
        # Get symptom connections
        connections = self.model.explain_symptom_connections(st.session_state.systems_medicine_state['reported_symptoms'])
        
        # Get potential patterns
        patterns = self.model.identify_multi_system_patterns(st.session_state.systems_medicine_state['reported_symptoms'])
        
        # Generate cross-specialty insights
        insights = {
            "specialties_involved": specialties_involved,
            "symptom_connections": connections.get("symptom_connections", []),
            "potential_patterns": patterns,
            "summary": self._generate_cross_specialty_summary(specialties_involved, connections, patterns)
        }
        
        return insights
    
    def _generate_cross_specialty_summary(self, specialties_involved, connections, patterns):
        """Generate a human-readable summary of cross-specialty insights."""
        summary = []
        
        # Summarize specialties involved
        if specialties_involved:
            specialties_text = ", ".join([specialty for specialty, _ in specialties_involved])
            summary.append(f"Your symptoms span multiple medical specialties including {specialties_text}.")
            summary.append("Rather than consulting each specialist separately, a unified approach that considers the interconnections between these areas would be more effective.")
        
        # Summarize key connections
        if "summary" in connections:
            summary.append(connections["summary"])
        
        # Summarize potential patterns
        if patterns:
            top_patterns = patterns[:2]
            patterns_text = ", ".join([pattern for pattern, _ in top_patterns])
            summary.append(f"Your symptoms suggest patterns consistent with {patterns_text}, which often require a multi-disciplinary approach.")
        
        # Add integrative medicine perspective
        summary.append("Modern medicine tends to compartmentalize treatment by specialty, but your health concerns demonstrate why an integrated approach is essential. Inflammation, diet, stress, and sleep can affect multiple body systems simultaneously, creating a complex web of symptoms that crosses traditional medical boundaries.")
        
        return " ".join(summary)
    
    def enhance_response(self, user_input, assistant_response):
        """
        Update the Systems Medicine model based on the conversation and enhance
        the assistant's response with cross-specialty insights.
        
        Args:
            user_input (str): The user's input message
            assistant_response (str): The assistant's response
        
        Returns:
            str: Enhanced assistant response
        """
        # Update the Systems Medicine model based on the conversation
        self.update_from_conversation(user_input, assistant_response)
        
        # Get holistic assessment
        assessment = self.get_holistic_assessment()
        
        # Get cross-specialty insights
        insights = self.get_cross_specialty_insights()
        
        # Check if we should enhance the response with cross-specialty insights
        should_enhance = self._should_enhance_with_insights(user_input, assistant_response)
        
        if should_enhance:
            # Create enhanced response
            enhanced_response = self._create_enhanced_response(assistant_response, insights)
            return enhanced_response
        else:
            # Return original response
            return assistant_response
    
    def _should_enhance_with_insights(self, user_input, assistant_response):
        """
        Determine if the response should be enhanced with cross-specialty insights.
        
        Args:
            user_input (str): The user's input message
            assistant_response (str): The assistant's response
        
        Returns:
            bool: Whether to enhance the response
        """
        # Check if there are enough symptoms to provide meaningful insights
        if len(st.session_state.systems_medicine_state['reported_symptoms']) < 2:
            return False
        
        # Check if multiple systems are involved
        affected_systems = st.session_state.systems_medicine_state['affected_systems']
        significant_systems = [system for system, score in affected_systems.items() if score >= 0.5]
        if len(significant_systems) < 2:
            return False
        
        # Check if the user is asking about connections or why they have multiple symptoms
        connection_patterns = [
            r"(?:why|how).*(?:related|connected|linked|associated)",
            r"(?:connection|relationship|link).*(?:between|among)",
            r"(?:multiple|different|various).*(?:symptoms|issues|problems)",
            r"(?:everything|all).*(?:connected|related|linked)",
            r"(?:see|understand|explain).*(?:big picture|overall|holistic)",
            r"(?:specialist|doctor).*(?:said|told|diagnosed)",
            r"(?:tried|seen|visited).*(?:different|multiple|many).*(?:doctors|specialists)"
        ]
        
        if any(re.search(pattern, user_input.lower()) for pattern in connection_patterns):
            return True
        
        # Check if the assistant's response mentions multiple systems or specialties
        specialty_mentions = sum(1 for specialty in ["neurologist", "gastroenterologist", "cardiologist", 
                                                    "endocrinologist", "rheumatologist", "immunologist", 
                                                    "psychiatrist", "dermatologist"] 
                                if specialty in assistant_response.lower())
        
        if specialty_mentions >= 2:
            return True
        
        # Check if the response mentions uncertainty or complexity
        uncertainty_patterns = [
            r"(?:complex|complicated|multifaceted)",
            r"(?:could be|might be|possibly).*(?:related|connected|linked)",
            r"(?:several|multiple|various).*(?:factors|causes|contributors)",
            r"(?:difficult|hard|challenging).*(?:determine|pinpoint|identify)"
        ]
        
        if any(re.search(pattern, assistant_response.lower()) for pattern in uncertainty_patterns):
            return True
        
        # By default, don't enhance
        return False
    
    def _create_enhanced_response(self, original_response, insights):
        """
        Create an enhanced response with cross-specialty insights.
        
        Args:
            original_response (str): The original assistant response
            insights (dict): Cross-specialty insights
        
        Returns:
            str: Enhanced response
        """
        # Start with the original response
        enhanced_response = original_response
        
        # Add a separator
        enhanced_response += "\n\n---\n\n"
        
        # Add cross-specialty insights
        enhanced_response += "**Unified Health Perspective:**\n\n"
        enhanced_response += insights["summary"]
        
        # Add specific connections if available
        if insights.get("symptom_connections") and len(insights["symptom_connections"]) > 0:
            enhanced_response += "\n\n**Key Symptom Connections:**\n"
            for i, conn in enumerate(insights["symptom_connections"][:2]):  # Top 2 connections
                shared_systems = ", ".join(conn["shared_systems"][:2])  # Top 2 shared systems
                enhanced_response += f"{i+1}. Your {conn['symptom1']} and {conn['symptom2']} are connected through the {shared_systems} systems.\n"
        
        # Add disclaimer
        enhanced_response += "\n\n*Note: This integrated perspective is meant to complement, not replace, traditional medical approaches. It highlights the interconnections between your symptoms that might be missed when each is addressed in isolation.*"
        
        return enhanced_response
    
    def get_next_question(self):
        """
        Get the next question to ask based on the Systems Medicine model.
        
        Returns:
            str: Next question to ask
        """
        # Get suggested symptoms to ask about
        suggested_symptoms = st.session_state.systems_medicine_state.get('suggested_questions', [])
        
        if not suggested_symptoms:
            return "Could you tell me more about how your symptoms affect your daily life?"
        
        # Get the top suggested symptom
        top_symptom = suggested_symptoms[0]
        
        # Format the question based on the symptom
        question_templates = {
            "Headache": "Have you been experiencing headaches? If so, could you describe their location, intensity, and any triggers you've noticed?",
            "Fatigue": "How is your energy level throughout the day? Do you experience unusual fatigue or exhaustion?",
            "Digestive Issues": "Have you noticed any changes in your digestion, such as bloating, discomfort, or changes in bowel habits?",
            "Sleep Problems": "How has your sleep been? Do you have trouble falling asleep, staying asleep, or do you wake up feeling unrefreshed?",
            "Mood Changes": "Have you noticed any changes in your mood, such as feeling more anxious, irritable, or down than usual?",
            "Pain": "Are you experiencing any pain or discomfort in your body? If so, where is it located and how would you describe it?",
            "Skin Issues": "Have you noticed any changes in your skin, such as rashes, dryness, or unusual sensations?",
            "Cognitive Function": "Have you experienced any changes in your thinking, memory, or concentration?",
            "Appetite Changes": "How has your appetite been? Have you noticed any changes in your hunger levels or food preferences?",
            "Weight Changes": "Have you experienced any unintentional weight changes recently?"
        }
        
        # Get the question for the top symptom
        if top_symptom in question_templates:
            return question_templates[top_symptom]
        else:
            # Generate a question based on the symptom
            return f"Have you been experiencing {top_symptom.lower()}? If so, could you tell me more about it?"
    
    def reset(self):
        """Reset the Systems Medicine model and session state."""
        st.session_state.systems_medicine_state = {
            'reported_symptoms': [],
            'asked_symptoms': [],
            'affected_systems': {},
            'lifestyle_factors': {},
            'suggested_questions': []
        }

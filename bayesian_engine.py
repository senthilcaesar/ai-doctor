import numpy as np
from collections import defaultdict
import math

class BayesianDiagnosisEngine:
    """
    A Bayesian reasoning engine for medical diagnosis that uses probabilistic inference
    to update beliefs about potential conditions based on observed symptoms.
    """
    
    def __init__(self, diseases=None, disease_priors=None, symptom_given_disease=None):
        """
        Initialize the Bayesian diagnosis engine with prior probabilities and conditional probabilities.
        
        Args:
            diseases (list, optional): List of disease names. Defaults to a predefined list.
            disease_priors (dict, optional): Prior probabilities of diseases. Defaults to predefined values.
            symptom_given_disease (dict, optional): Conditional probabilities of symptoms given diseases.
                                                   Defaults to predefined values.
        """
        # Default diseases if none provided
        self.diseases = diseases or [
            "Common Cold", "Influenza", "COVID-19", "Allergic Rhinitis", 
            "Sinusitis", "Bronchitis", "Pneumonia", "Asthma", "GERD", 
            "Migraine", "Tension Headache", "UTI", "Gastroenteritis"
        ]
        
        # Default prior probabilities if none provided
        self.disease_priors = disease_priors or {
            "Common Cold": 0.20,
            "Influenza": 0.10,
            "COVID-19": 0.05,
            "Allergic Rhinitis": 0.15,
            "Sinusitis": 0.08,
            "Bronchitis": 0.07,
            "Pneumonia": 0.03,
            "Asthma": 0.06,
            "GERD": 0.08,
            "Migraine": 0.09,
            "Tension Headache": 0.12,
            "UTI": 0.04,
            "Gastroenteritis": 0.10
        }
        
        # Default conditional probabilities if none provided
        self.symptom_given_disease = symptom_given_disease or {
            "Fever": {
                "Common Cold": 0.40, "Influenza": 0.90, "COVID-19": 0.80,
                "Allergic Rhinitis": 0.05, "Sinusitis": 0.30, "Bronchitis": 0.40,
                "Pneumonia": 0.85, "Asthma": 0.10, "GERD": 0.01,
                "Migraine": 0.15, "Tension Headache": 0.05, "UTI": 0.40,
                "Gastroenteritis": 0.50
            },
            "Cough": {
                "Common Cold": 0.80, "Influenza": 0.80, "COVID-19": 0.80,
                "Allergic Rhinitis": 0.30, "Sinusitis": 0.40, "Bronchitis": 0.90,
                "Pneumonia": 0.90, "Asthma": 0.70, "GERD": 0.40,
                "Migraine": 0.05, "Tension Headache": 0.05, "UTI": 0.01,
                "Gastroenteritis": 0.10
            },
            "Shortness of Breath": {
                "Common Cold": 0.10, "Influenza": 0.20, "COVID-19": 0.60,
                "Allergic Rhinitis": 0.20, "Sinusitis": 0.05, "Bronchitis": 0.70,
                "Pneumonia": 0.90, "Asthma": 0.95, "GERD": 0.20,
                "Migraine": 0.05, "Tension Headache": 0.05, "UTI": 0.01,
                "Gastroenteritis": 0.05
            },
            "Fatigue": {
                "Common Cold": 0.70, "Influenza": 0.90, "COVID-19": 0.85,
                "Allergic Rhinitis": 0.40, "Sinusitis": 0.60, "Bronchitis": 0.70,
                "Pneumonia": 0.90, "Asthma": 0.50, "GERD": 0.30,
                "Migraine": 0.80, "Tension Headache": 0.70, "UTI": 0.60,
                "Gastroenteritis": 0.80
            },
            "Headache": {
                "Common Cold": 0.60, "Influenza": 0.80, "COVID-19": 0.70,
                "Allergic Rhinitis": 0.60, "Sinusitis": 0.85, "Bronchitis": 0.30,
                "Pneumonia": 0.40, "Asthma": 0.20, "GERD": 0.20,
                "Migraine": 0.95, "Tension Headache": 0.95, "UTI": 0.30,
                "Gastroenteritis": 0.50
            },
            "Sore Throat": {
                "Common Cold": 0.80, "Influenza": 0.60, "COVID-19": 0.60,
                "Allergic Rhinitis": 0.30, "Sinusitis": 0.40, "Bronchitis": 0.50,
                "Pneumonia": 0.30, "Asthma": 0.10, "GERD": 0.60,
                "Migraine": 0.05, "Tension Headache": 0.05, "UTI": 0.01,
                "Gastroenteritis": 0.10
            },
            "Runny Nose": {
                "Common Cold": 0.90, "Influenza": 0.60, "COVID-19": 0.50,
                "Allergic Rhinitis": 0.95, "Sinusitis": 0.80, "Bronchitis": 0.30,
                "Pneumonia": 0.10, "Asthma": 0.20, "GERD": 0.01,
                "Migraine": 0.10, "Tension Headache": 0.05, "UTI": 0.01,
                "Gastroenteritis": 0.05
            },
            "Nasal Congestion": {
                "Common Cold": 0.90, "Influenza": 0.60, "COVID-19": 0.50,
                "Allergic Rhinitis": 0.90, "Sinusitis": 0.90, "Bronchitis": 0.20,
                "Pneumonia": 0.10, "Asthma": 0.20, "GERD": 0.01,
                "Migraine": 0.20, "Tension Headache": 0.10, "UTI": 0.01,
                "Gastroenteritis": 0.05
            },
            "Sneezing": {
                "Common Cold": 0.80, "Influenza": 0.40, "COVID-19": 0.30,
                "Allergic Rhinitis": 0.95, "Sinusitis": 0.60, "Bronchitis": 0.20,
                "Pneumonia": 0.10, "Asthma": 0.30, "GERD": 0.01,
                "Migraine": 0.10, "Tension Headache": 0.05, "UTI": 0.01,
                "Gastroenteritis": 0.05
            },
            "Chest Pain": {
                "Common Cold": 0.10, "Influenza": 0.20, "COVID-19": 0.40,
                "Allergic Rhinitis": 0.05, "Sinusitis": 0.05, "Bronchitis": 0.60,
                "Pneumonia": 0.70, "Asthma": 0.60, "GERD": 0.70,
                "Migraine": 0.10, "Tension Headache": 0.05, "UTI": 0.01,
                "Gastroenteritis": 0.10
            },
            "Wheezing": {
                "Common Cold": 0.10, "Influenza": 0.10, "COVID-19": 0.30,
                "Allergic Rhinitis": 0.30, "Sinusitis": 0.05, "Bronchitis": 0.70,
                "Pneumonia": 0.60, "Asthma": 0.95, "GERD": 0.10,
                "Migraine": 0.01, "Tension Headache": 0.01, "UTI": 0.01,
                "Gastroenteritis": 0.01
            },
            "Nausea": {
                "Common Cold": 0.20, "Influenza": 0.60, "COVID-19": 0.50,
                "Allergic Rhinitis": 0.10, "Sinusitis": 0.30, "Bronchitis": 0.10,
                "Pneumonia": 0.30, "Asthma": 0.10, "GERD": 0.80,
                "Migraine": 0.70, "Tension Headache": 0.30, "UTI": 0.30,
                "Gastroenteritis": 0.90
            },
            "Vomiting": {
                "Common Cold": 0.10, "Influenza": 0.50, "COVID-19": 0.30,
                "Allergic Rhinitis": 0.05, "Sinusitis": 0.20, "Bronchitis": 0.05,
                "Pneumonia": 0.20, "Asthma": 0.05, "GERD": 0.60,
                "Migraine": 0.60, "Tension Headache": 0.10, "UTI": 0.20,
                "Gastroenteritis": 0.90
            },
            "Diarrhea": {
                "Common Cold": 0.05, "Influenza": 0.30, "COVID-19": 0.40,
                "Allergic Rhinitis": 0.01, "Sinusitis": 0.05, "Bronchitis": 0.05,
                "Pneumonia": 0.10, "Asthma": 0.01, "GERD": 0.30,
                "Migraine": 0.10, "Tension Headache": 0.05, "UTI": 0.10,
                "Gastroenteritis": 0.95
            },
            "Abdominal Pain": {
                "Common Cold": 0.05, "Influenza": 0.30, "COVID-19": 0.20,
                "Allergic Rhinitis": 0.01, "Sinusitis": 0.05, "Bronchitis": 0.05,
                "Pneumonia": 0.10, "Asthma": 0.01, "GERD": 0.70,
                "Migraine": 0.20, "Tension Headache": 0.05, "UTI": 0.40,
                "Gastroenteritis": 0.90
            },
            "Muscle Aches": {
                "Common Cold": 0.50, "Influenza": 0.90, "COVID-19": 0.70,
                "Allergic Rhinitis": 0.10, "Sinusitis": 0.30, "Bronchitis": 0.40,
                "Pneumonia": 0.60, "Asthma": 0.10, "GERD": 0.05,
                "Migraine": 0.40, "Tension Headache": 0.60, "UTI": 0.30,
                "Gastroenteritis": 0.40
            },
            "Joint Pain": {
                "Common Cold": 0.30, "Influenza": 0.80, "COVID-19": 0.60,
                "Allergic Rhinitis": 0.05, "Sinusitis": 0.20, "Bronchitis": 0.20,
                "Pneumonia": 0.30, "Asthma": 0.05, "GERD": 0.05,
                "Migraine": 0.20, "Tension Headache": 0.30, "UTI": 0.20,
                "Gastroenteritis": 0.20
            },
            "Chills": {
                "Common Cold": 0.40, "Influenza": 0.90, "COVID-19": 0.80,
                "Allergic Rhinitis": 0.05, "Sinusitis": 0.30, "Bronchitis": 0.40,
                "Pneumonia": 0.80, "Asthma": 0.10, "GERD": 0.01,
                "Migraine": 0.20, "Tension Headache": 0.10, "UTI": 0.40,
                "Gastroenteritis": 0.50
            },
            "Loss of Taste/Smell": {
                "Common Cold": 0.30, "Influenza": 0.20, "COVID-19": 0.80,
                "Allergic Rhinitis": 0.40, "Sinusitis": 0.60, "Bronchitis": 0.05,
                "Pneumonia": 0.10, "Asthma": 0.01, "GERD": 0.10,
                "Migraine": 0.20, "Tension Headache": 0.05, "UTI": 0.01,
                "Gastroenteritis": 0.05
            },
            "Itchy Eyes": {
                "Common Cold": 0.30, "Influenza": 0.10, "COVID-19": 0.10,
                "Allergic Rhinitis": 0.90, "Sinusitis": 0.40, "Bronchitis": 0.05,
                "Pneumonia": 0.05, "Asthma": 0.20, "GERD": 0.01,
                "Migraine": 0.30, "Tension Headache": 0.10, "UTI": 0.01,
                "Gastroenteritis": 0.01
            },
            "Ear Pain": {
                "Common Cold": 0.40, "Influenza": 0.20, "COVID-19": 0.10,
                "Allergic Rhinitis": 0.20, "Sinusitis": 0.60, "Bronchitis": 0.05,
                "Pneumonia": 0.05, "Asthma": 0.01, "GERD": 0.05,
                "Migraine": 0.30, "Tension Headache": 0.20, "UTI": 0.01,
                "Gastroenteritis": 0.01
            },
            "Frequent Urination": {
                "Common Cold": 0.05, "Influenza": 0.05, "COVID-19": 0.05,
                "Allergic Rhinitis": 0.01, "Sinusitis": 0.01, "Bronchitis": 0.01,
                "Pneumonia": 0.05, "Asthma": 0.01, "GERD": 0.05,
                "Migraine": 0.01, "Tension Headache": 0.01, "UTI": 0.95,
                "Gastroenteritis": 0.10
            },
            "Painful Urination": {
                "Common Cold": 0.01, "Influenza": 0.01, "COVID-19": 0.01,
                "Allergic Rhinitis": 0.01, "Sinusitis": 0.01, "Bronchitis": 0.01,
                "Pneumonia": 0.01, "Asthma": 0.01, "GERD": 0.01,
                "Migraine": 0.01, "Tension Headache": 0.01, "UTI": 0.95,
                "Gastroenteritis": 0.05
            },
            "Blood in Urine": {
                "Common Cold": 0.01, "Influenza": 0.01, "COVID-19": 0.01,
                "Allergic Rhinitis": 0.01, "Sinusitis": 0.01, "Bronchitis": 0.01,
                "Pneumonia": 0.01, "Asthma": 0.01, "GERD": 0.01,
                "Migraine": 0.01, "Tension Headache": 0.01, "UTI": 0.40,
                "Gastroenteritis": 0.05
            },
            "Heartburn": {
                "Common Cold": 0.05, "Influenza": 0.05, "COVID-19": 0.10,
                "Allergic Rhinitis": 0.01, "Sinusitis": 0.05, "Bronchitis": 0.05,
                "Pneumonia": 0.05, "Asthma": 0.05, "GERD": 0.95,
                "Migraine": 0.10, "Tension Headache": 0.05, "UTI": 0.01,
                "Gastroenteritis": 0.20
            },
            "Regurgitation": {
                "Common Cold": 0.05, "Influenza": 0.10, "COVID-19": 0.05,
                "Allergic Rhinitis": 0.01, "Sinusitis": 0.05, "Bronchitis": 0.05,
                "Pneumonia": 0.05, "Asthma": 0.05, "GERD": 0.90,
                "Migraine": 0.10, "Tension Headache": 0.05, "UTI": 0.01,
                "Gastroenteritis": 0.60
            },
            "Light Sensitivity": {
                "Common Cold": 0.10, "Influenza": 0.30, "COVID-19": 0.20,
                "Allergic Rhinitis": 0.30, "Sinusitis": 0.40, "Bronchitis": 0.05,
                "Pneumonia": 0.10, "Asthma": 0.05, "GERD": 0.05,
                "Migraine": 0.90, "Tension Headache": 0.60, "UTI": 0.05,
                "Gastroenteritis": 0.10
            },
            "Sound Sensitivity": {
                "Common Cold": 0.10, "Influenza": 0.20, "COVID-19": 0.10,
                "Allergic Rhinitis": 0.10, "Sinusitis": 0.30, "Bronchitis": 0.05,
                "Pneumonia": 0.05, "Asthma": 0.05, "GERD": 0.05,
                "Migraine": 0.85, "Tension Headache": 0.50, "UTI": 0.05,
                "Gastroenteritis": 0.05
            }
        }
        
        # Validate that all diseases in disease_priors are in the list of diseases
        for disease in self.disease_priors:
            if disease not in self.diseases:
                self.diseases.append(disease)
        
        # Validate that all diseases in symptom_given_disease are in the list of diseases
        for symptom in self.symptom_given_disease:
            for disease in self.symptom_given_disease[symptom]:
                if disease not in self.diseases:
                    self.diseases.append(disease)
        
        # Initialize current belief state (posterior probabilities)
        self.beliefs = self.disease_priors.copy()
        
        # Normalize beliefs to ensure they sum to 1
        self._normalize_beliefs()
        
        # Observed symptoms and their values (True for present, False for absent)
        self.observed_symptoms = {}
    
    def _normalize_beliefs(self):
        """Normalize the belief probabilities to ensure they sum to 1."""
        total = sum(self.beliefs.values())
        if total > 0:  # Avoid division by zero
            for disease in self.beliefs:
                self.beliefs[disease] /= total
    
    def update_belief(self, symptom, has_symptom):
        """
        Update beliefs using Bayes' rule based on symptom observation.
        
        Args:
            symptom (str): The symptom being observed
            has_symptom (bool): Whether the symptom is present (True) or absent (False)
        
        Returns:
            dict: Updated belief state
        """
        # Check if the symptom is in our knowledge base
        if symptom not in self.symptom_given_disease:
            return self.beliefs
        
        # Record the observation
        self.observed_symptoms[symptom] = has_symptom
        
        # Calculate likelihood: P(symptom|disease) or P(¬symptom|disease)
        likelihoods = {}
        for disease in self.diseases:
            if disease in self.symptom_given_disease[symptom]:
                if has_symptom:
                    likelihoods[disease] = self.symptom_given_disease[symptom][disease]
                else:
                    likelihoods[disease] = 1 - self.symptom_given_disease[symptom][disease]
            else:
                # Default value if disease is not in the conditional probability table
                likelihoods[disease] = 0.5  # Neutral likelihood
        
        # Calculate evidence: P(symptom)
        evidence = sum(self.beliefs[disease] * likelihoods[disease] for disease in self.diseases 
                      if disease in self.beliefs and disease in likelihoods)
        
        # Avoid division by zero
        if evidence == 0:
            return self.beliefs
        
        # Apply Bayes' rule: P(disease|symptom) = P(symptom|disease) * P(disease) / P(symptom)
        for disease in self.diseases:
            if disease in self.beliefs and disease in likelihoods:
                self.beliefs[disease] = (likelihoods[disease] * self.beliefs[disease]) / evidence
        
        # Normalize beliefs
        self._normalize_beliefs()
        
        return self.beliefs
    
    def get_diagnosis(self, threshold=0.0):
        """
        Return diseases above a certain probability threshold.
        
        Args:
            threshold (float, optional): Minimum probability threshold. Defaults to 0.0.
        
        Returns:
            list: List of (disease, probability) tuples sorted by probability (descending)
        """
        # Filter diseases by threshold and sort by probability (descending)
        diagnosis = [(disease, prob) for disease, prob in self.beliefs.items() if prob >= threshold]
        diagnosis.sort(key=lambda x: x[1], reverse=True)
        return diagnosis
    
    def get_top_diagnoses(self, n=3):
        """
        Return the top N most likely diagnoses.
        
        Args:
            n (int, optional): Number of diagnoses to return. Defaults to 3.
        
        Returns:
            list: List of (disease, probability) tuples for the top N diagnoses
        """
        diagnosis = self.get_diagnosis()
        return diagnosis[:n]
    
    def calculate_information_gain(self, symptom):
        """
        Calculate the expected information gain from asking about a symptom.
        
        Args:
            symptom (str): The symptom to calculate information gain for
        
        Returns:
            float: Expected information gain (in bits)
        """
        # Skip if symptom is already observed
        if symptom in self.observed_symptoms:
            return 0.0
        
        # Skip if symptom is not in our knowledge base
        if symptom not in self.symptom_given_disease:
            return 0.0
        
        # Calculate current entropy
        current_entropy = self.calculate_entropy(self.beliefs)
        
        # Calculate expected entropy after observing the symptom
        expected_entropy = 0.0
        
        # For symptom present (has_symptom = True)
        # Calculate P(symptom = True)
        p_symptom_true = sum(self.beliefs[disease] * self.symptom_given_disease[symptom][disease]
                            for disease in self.diseases if disease in self.beliefs and disease in self.symptom_given_disease[symptom])
        
        if p_symptom_true > 0:
            # Calculate posterior beliefs if symptom is present
            posterior_true = {}
            for disease in self.diseases:
                if disease in self.beliefs and disease in self.symptom_given_disease[symptom]:
                    likelihood = self.symptom_given_disease[symptom][disease]
                    posterior_true[disease] = (likelihood * self.beliefs[disease]) / p_symptom_true
            
            # Calculate entropy of posterior beliefs
            entropy_true = self.calculate_entropy(posterior_true)
            expected_entropy += p_symptom_true * entropy_true
        
        # For symptom absent (has_symptom = False)
        # Calculate P(symptom = False)
        p_symptom_false = sum(self.beliefs[disease] * (1 - self.symptom_given_disease[symptom][disease])
                             for disease in self.diseases if disease in self.beliefs and disease in self.symptom_given_disease[symptom])
        
        if p_symptom_false > 0:
            # Calculate posterior beliefs if symptom is absent
            posterior_false = {}
            for disease in self.diseases:
                if disease in self.beliefs and disease in self.symptom_given_disease[symptom]:
                    likelihood = 1 - self.symptom_given_disease[symptom][disease]
                    posterior_false[disease] = (likelihood * self.beliefs[disease]) / p_symptom_false
            
            # Calculate entropy of posterior beliefs
            entropy_false = self.calculate_entropy(posterior_false)
            expected_entropy += p_symptom_false * entropy_false
        
        # Information gain = current entropy - expected entropy
        information_gain = current_entropy - expected_entropy
        return information_gain
    
    def calculate_entropy(self, probabilities):
        """
        Calculate the entropy of a probability distribution.
        
        Args:
            probabilities (dict): Dictionary of probabilities
        
        Returns:
            float: Entropy value (in bits)
        """
        entropy = 0.0
        for p in probabilities.values():
            if p > 0:  # Avoid log(0)
                entropy -= p * math.log2(p)
        return entropy
    
    def suggest_questions(self, n=3):
        """
        Suggest the next symptoms to ask about to maximize information gain.
        
        Args:
            n (int, optional): Number of symptoms to suggest. Defaults to 3.
        
        Returns:
            list: List of (symptom, information_gain) tuples sorted by information gain (descending)
        """
        # Calculate information gain for each unobserved symptom
        information_gains = []
        for symptom in self.symptom_given_disease:
            if symptom not in self.observed_symptoms:
                gain = self.calculate_information_gain(symptom)
                information_gains.append((symptom, gain))
        
        # Sort by information gain (descending)
        information_gains.sort(key=lambda x: x[1], reverse=True)
        
        return information_gains[:n]
    
    def reset(self):
        """Reset the engine to initial state."""
        self.beliefs = self.disease_priors.copy()
        self._normalize_beliefs()
        self.observed_symptoms = {}
        return self.beliefs
    
    def get_confidence(self):
        """
        Return the confidence level in the top diagnosis.
        
        Returns:
            float: Confidence level (0.0 to 1.0)
        """
        diagnosis = self.get_top_diagnoses(1)
        if diagnosis:
            return diagnosis[0][1]
        return 0.0
    
    def get_differential_diagnosis(self, n=3):
        """
        Return a differential diagnosis with explanations.
        
        Args:
            n (int, optional): Number of diagnoses to include. Defaults to 3.
        
        Returns:
            list: List of dictionaries with disease, probability, and supporting evidence
        """
        top_diagnoses = self.get_top_diagnoses(n)
        differential = []
        
        for disease, probability in top_diagnoses:
            # Find supporting evidence (symptoms that support this diagnosis)
            supporting_evidence = []
            contradicting_evidence = []
            
            for symptom, has_symptom in self.observed_symptoms.items():
                if symptom in self.symptom_given_disease and disease in self.symptom_given_disease[symptom]:
                    symptom_prob = self.symptom_given_disease[symptom][disease]
                    
                    if has_symptom and symptom_prob > 0.5:
                        # Symptom is present and supports this disease
                        supporting_evidence.append({
                            "symptom": symptom,
                            "probability": symptom_prob,
                            "strength": "strong" if symptom_prob > 0.8 else "moderate" if symptom_prob > 0.6 else "mild"
                        })
                    elif not has_symptom and symptom_prob < 0.5:
                        # Symptom is absent and supports this disease (by its absence)
                        supporting_evidence.append({
                            "symptom": f"absence of {symptom}",
                            "probability": 1 - symptom_prob,
                            "strength": "strong" if symptom_prob < 0.2 else "moderate" if symptom_prob < 0.4 else "mild"
                        })
                    elif has_symptom and symptom_prob < 0.5:
                        # Symptom is present but contradicts this disease
                        contradicting_evidence.append({
                            "symptom": symptom,
                            "probability": symptom_prob,
                            "strength": "strong" if symptom_prob < 0.2 else "moderate" if symptom_prob < 0.4 else "mild"
                        })
                    elif not has_symptom and symptom_prob > 0.5:
                        # Symptom is absent but contradicts this disease (should be present)
                        contradicting_evidence.append({
                            "symptom": f"absence of {symptom}",
                            "probability": symptom_prob,
                            "strength": "strong" if symptom_prob > 0.8 else "moderate" if symptom_prob > 0.6 else "mild"
                        })
            
            # Sort evidence by strength
            supporting_evidence.sort(key=lambda x: x["probability"], reverse=True)
            contradicting_evidence.sort(key=lambda x: 1 - x["probability"], reverse=True)
            
            differential.append({
                "disease": disease,
                "probability": probability,
                "supporting_evidence": supporting_evidence,
                "contradicting_evidence": contradicting_evidence
            })
        
        return differential
    
    def explain_reasoning(self, disease):
        """
        Explain the reasoning behind a specific diagnosis.
        
        Args:
            disease (str): The disease to explain
        
        Returns:
            dict: Explanation including prior probability, likelihood, and posterior probability
        """
        if disease not in self.beliefs:
            return {
                "disease": disease,
                "explanation": "Disease not in knowledge base",
                "prior_probability": 0.0,
                "posterior_probability": 0.0,
                "evidence_factors": []
            }
        
        # Get prior and posterior probabilities
        prior_probability = self.disease_priors.get(disease, 0.0)
        posterior_probability = self.beliefs[disease]
        
        # Calculate likelihood factors for each observed symptom
        evidence_factors = []
        for symptom, has_symptom in self.observed_symptoms.items():
            if symptom in self.symptom_given_disease and disease in self.symptom_given_disease[symptom]:
                # Get the conditional probability
                p_symptom_given_disease = self.symptom_given_disease[symptom][disease]
                
                # Calculate the likelihood factor
                if has_symptom:
                    likelihood = p_symptom_given_disease
                    effect = "supporting" if likelihood > 0.5 else "contradicting"
                    strength = "strong" if abs(likelihood - 0.5) > 0.3 else "moderate" if abs(likelihood - 0.5) > 0.1 else "mild"
                else:
                    likelihood = 1 - p_symptom_given_disease
                    effect = "supporting" if likelihood > 0.5 else "contradicting"
                    strength = "strong" if abs(likelihood - 0.5) > 0.3 else "moderate" if abs(likelihood - 0.5) > 0.1 else "mild"
                
                evidence_factors.append({
                    "symptom": symptom,
                    "present": has_symptom,
                    "conditional_probability": p_symptom_given_disease,
                    "likelihood_factor": likelihood,
                    "effect": effect,
                    "strength": strength
                })
        
        # Sort evidence factors by strength of effect
        evidence_factors.sort(key=lambda x: abs(x["likelihood_factor"] - 0.5), reverse=True)
        
        # Generate explanation text
        explanation = f"The diagnosis of {disease} has a posterior probability of {posterior_probability:.2f} "
        explanation += f"(prior: {prior_probability:.2f}). "
        
        if evidence_factors:
            explanation += "Key factors: "
            for factor in evidence_factors[:3]:  # Top 3 factors
                symptom_status = "presence" if factor["present"] else "absence"
                explanation += f"The {symptom_status} of {factor['symptom']} is a {factor['strength']} "
                explanation += f"{factor['effect']} factor (likelihood: {factor['likelihood_factor']:.2f}). "
        
        return {
            "disease": disease,
            "explanation": explanation,
            "prior_probability": prior_probability,
            "posterior_probability": posterior_probability,
            "evidence_factors": evidence_factors
        }

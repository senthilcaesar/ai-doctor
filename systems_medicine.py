import numpy as np
from collections import defaultdict
import math

class SystemsMedicineModel:
    """
    A systems medicine model that represents the interconnections between different body systems
    and provides methods for cross-domain symptom analysis and holistic health assessment.
    """
    
    def __init__(self):
        """Initialize the systems medicine model with body systems and their interconnections."""
        # Define body systems
        self.body_systems = [
            "Neurological",      # Brain, nerves, cognitive function
            "Endocrine",         # Hormones, metabolism
            "Immune",            # Immune response, inflammation
            "Digestive",         # Gut, digestion, absorption
            "Cardiovascular",    # Heart, blood vessels, circulation
            "Respiratory",       # Lungs, breathing
            "Musculoskeletal",   # Muscles, bones, joints
            "Integumentary",     # Skin, hair, nails
            "Urinary",           # Kidneys, bladder, urine production
            "Reproductive",      # Reproductive organs and functions
            "Mental Health",     # Psychological and emotional state
            "Metabolic"          # Energy production, nutrient processing
        ]
        
        # Define system interconnections (bidirectional influence strength from 0 to 1)
        # This represents how strongly systems influence each other
        self.system_connections = {
            ("Neurological", "Endocrine"): 0.8,        # Strong neuroendocrine connection
            ("Neurological", "Immune"): 0.7,           # Psychoneuroimmunology
            ("Neurological", "Digestive"): 0.7,        # Gut-brain axis
            ("Neurological", "Mental Health"): 0.9,    # Brain-mind connection
            ("Neurological", "Cardiovascular"): 0.6,   # Neurocardiac axis
            ("Neurological", "Respiratory"): 0.6,      # Breathing control
            ("Neurological", "Musculoskeletal"): 0.5,  # Motor control
            
            ("Endocrine", "Immune"): 0.7,              # Hormones affect immune function
            ("Endocrine", "Digestive"): 0.6,           # Gut hormones
            ("Endocrine", "Metabolic"): 0.9,           # Hormones regulate metabolism
            ("Endocrine", "Cardiovascular"): 0.7,      # Hormones affect heart function
            ("Endocrine", "Reproductive"): 0.8,        # Reproductive hormones
            ("Endocrine", "Mental Health"): 0.7,       # Hormones affect mood
            
            ("Immune", "Digestive"): 0.8,              # Gut immunity
            ("Immune", "Respiratory"): 0.7,            # Respiratory immunity
            ("Immune", "Integumentary"): 0.7,          # Skin immunity
            ("Immune", "Mental Health"): 0.6,          # Inflammation affects mood
            ("Immune", "Metabolic"): 0.6,              # Immune-metabolic interactions
            
            ("Digestive", "Metabolic"): 0.8,           # Nutrient absorption
            ("Digestive", "Immune"): 0.8,              # Gut microbiome affects immunity
            ("Digestive", "Mental Health"): 0.7,       # Gut-brain axis
            
            ("Cardiovascular", "Respiratory"): 0.8,    # Cardiopulmonary system
            ("Cardiovascular", "Metabolic"): 0.7,      # Cardiovascular-metabolic syndrome
            ("Cardiovascular", "Urinary"): 0.6,        # Blood pressure regulation
            
            ("Respiratory", "Cardiovascular"): 0.8,    # Oxygen delivery
            ("Respiratory", "Immune"): 0.7,            # Respiratory immunity
            
            ("Musculoskeletal", "Metabolic"): 0.6,     # Exercise affects metabolism
            ("Musculoskeletal", "Cardiovascular"): 0.6, # Exercise affects heart
            
            ("Metabolic", "Endocrine"): 0.9,           # Metabolic feedback to hormones
            ("Metabolic", "Immune"): 0.6,              # Metabolic inflammation
            ("Metabolic", "Cardiovascular"): 0.7,      # Metabolic syndrome
            
            ("Mental Health", "Neurological"): 0.9,    # Mind-brain connection
            ("Mental Health", "Endocrine"): 0.7,       # Stress affects hormones
            ("Mental Health", "Immune"): 0.6,          # Stress affects immunity
            ("Mental Health", "Digestive"): 0.7,       # Stress affects digestion
        }
        
        # Make connections bidirectional if not already defined
        bidirectional_connections = {}
        for (sys1, sys2), strength in self.system_connections.items():
            bidirectional_connections[(sys1, sys2)] = strength
            # If reverse connection not already defined, add it with same strength
            if (sys2, sys1) not in self.system_connections:
                bidirectional_connections[(sys2, sys1)] = strength
        
        self.system_connections = bidirectional_connections
        
        # Define common symptoms and their primary and secondary system associations
        # Format: "Symptom": {"primary_system": weight, "secondary_system1": weight, ...}
        # Weight represents the strength of association (0 to 1)
        self.symptom_system_mapping = {
            # Neurological symptoms
            "Headache": {
                "Neurological": 0.9, 
                "Cardiovascular": 0.6, 
                "Endocrine": 0.5, 
                "Immune": 0.4, 
                "Digestive": 0.3
            },
            "Dizziness": {
                "Neurological": 0.8, 
                "Cardiovascular": 0.7, 
                "Endocrine": 0.4, 
                "Respiratory": 0.3
            },
            "Fatigue": {
                "Neurological": 0.6, 
                "Endocrine": 0.7, 
                "Immune": 0.7, 
                "Metabolic": 0.8, 
                "Mental Health": 0.6, 
                "Cardiovascular": 0.5
            },
            "Memory Problems": {
                "Neurological": 0.9, 
                "Endocrine": 0.5, 
                "Cardiovascular": 0.4, 
                "Mental Health": 0.6
            },
            "Numbness/Tingling": {
                "Neurological": 0.9, 
                "Cardiovascular": 0.4, 
                "Endocrine": 0.5, 
                "Immune": 0.3
            },
            
            # Digestive symptoms
            "Abdominal Pain": {
                "Digestive": 0.9, 
                "Reproductive": 0.5, 
                "Urinary": 0.4, 
                "Immune": 0.3
            },
            "Nausea": {
                "Digestive": 0.8, 
                "Neurological": 0.5, 
                "Endocrine": 0.4, 
                "Mental Health": 0.3
            },
            "Diarrhea": {
                "Digestive": 0.9, 
                "Immune": 0.6, 
                "Endocrine": 0.3
            },
            "Constipation": {
                "Digestive": 0.9, 
                "Neurological": 0.4, 
                "Metabolic": 0.4, 
                "Endocrine": 0.3
            },
            "Bloating": {
                "Digestive": 0.9, 
                "Immune": 0.5, 
                "Endocrine": 0.3, 
                "Metabolic": 0.3
            },
            "Acid Reflux": {
                "Digestive": 0.9, 
                "Respiratory": 0.4, 
                "Cardiovascular": 0.3
            },
            
            # Cardiovascular symptoms
            "Chest Pain": {
                "Cardiovascular": 0.9, 
                "Respiratory": 0.7, 
                "Digestive": 0.4, 
                "Musculoskeletal": 0.4, 
                "Mental Health": 0.3
            },
            "Palpitations": {
                "Cardiovascular": 0.9, 
                "Endocrine": 0.6, 
                "Mental Health": 0.5, 
                "Neurological": 0.3
            },
            "Shortness of Breath": {
                "Respiratory": 0.9, 
                "Cardiovascular": 0.8, 
                "Immune": 0.4, 
                "Mental Health": 0.4
            },
            "Edema": {
                "Cardiovascular": 0.8, 
                "Urinary": 0.6, 
                "Endocrine": 0.4, 
                "Immune": 0.3
            },
            
            # Immune symptoms
            "Fever": {
                "Immune": 0.9, 
                "Respiratory": 0.6, 
                "Digestive": 0.5, 
                "Urinary": 0.4
            },
            "Joint Pain": {
                "Musculoskeletal": 0.9, 
                "Immune": 0.7, 
                "Endocrine": 0.4
            },
            "Rash": {
                "Integumentary": 0.9, 
                "Immune": 0.8, 
                "Digestive": 0.3, 
                "Endocrine": 0.3
            },
            "Recurrent Infections": {
                "Immune": 0.9, 
                "Respiratory": 0.6, 
                "Urinary": 0.5, 
                "Integumentary": 0.4
            },
            
            # Endocrine symptoms
            "Weight Changes": {
                "Endocrine": 0.8, 
                "Metabolic": 0.8, 
                "Digestive": 0.5, 
                "Mental Health": 0.4
            },
            "Heat/Cold Intolerance": {
                "Endocrine": 0.9, 
                "Metabolic": 0.7, 
                "Cardiovascular": 0.4
            },
            "Excessive Thirst": {
                "Endocrine": 0.8, 
                "Metabolic": 0.7, 
                "Urinary": 0.6
            },
            "Hair Loss": {
                "Endocrine": 0.7, 
                "Integumentary": 0.8, 
                "Immune": 0.5, 
                "Metabolic": 0.4
            },
            
            # Mental health symptoms
            "Anxiety": {
                "Mental Health": 0.9, 
                "Neurological": 0.7, 
                "Endocrine": 0.6, 
                "Cardiovascular": 0.5, 
                "Digestive": 0.4
            },
            "Depression": {
                "Mental Health": 0.9, 
                "Neurological": 0.7, 
                "Endocrine": 0.6, 
                "Immune": 0.5, 
                "Metabolic": 0.4
            },
            "Insomnia": {
                "Mental Health": 0.8, 
                "Neurological": 0.7, 
                "Endocrine": 0.6, 
                "Metabolic": 0.4
            },
            "Irritability": {
                "Mental Health": 0.8, 
                "Neurological": 0.6, 
                "Endocrine": 0.7, 
                "Digestive": 0.4
            },
            
            # Respiratory symptoms
            "Cough": {
                "Respiratory": 0.9, 
                "Immune": 0.7, 
                "Digestive": 0.3
            },
            "Wheezing": {
                "Respiratory": 0.9, 
                "Immune": 0.7, 
                "Cardiovascular": 0.3
            },
            
            # Urinary symptoms
            "Frequent Urination": {
                "Urinary": 0.9, 
                "Endocrine": 0.7, 
                "Reproductive": 0.4
            },
            "Urinary Pain": {
                "Urinary": 0.9, 
                "Immune": 0.6, 
                "Reproductive": 0.4
            },
            
            # Musculoskeletal symptoms
            "Back Pain": {
                "Musculoskeletal": 0.9, 
                "Neurological": 0.6, 
                "Urinary": 0.3, 
                "Reproductive": 0.3
            },
            "Muscle Weakness": {
                "Musculoskeletal": 0.8, 
                "Neurological": 0.7, 
                "Endocrine": 0.6, 
                "Metabolic": 0.5
            }
        }
        
        # Define lifestyle factors and their impact on body systems
        # Format: "Factor": {"system": impact_strength, ...}
        # Impact strength can be positive (beneficial) or negative (harmful)
        self.lifestyle_system_impact = {
            "Diet": {
                "Digestive": 0.9,
                "Immune": 0.8,
                "Metabolic": 0.9,
                "Cardiovascular": 0.8,
                "Endocrine": 0.7,
                "Neurological": 0.6,
                "Mental Health": 0.6
            },
            "Sleep": {
                "Neurological": 0.9,
                "Endocrine": 0.8,
                "Immune": 0.7,
                "Mental Health": 0.8,
                "Metabolic": 0.7,
                "Cardiovascular": 0.6
            },
            "Exercise": {
                "Musculoskeletal": 0.9,
                "Cardiovascular": 0.9,
                "Metabolic": 0.8,
                "Immune": 0.7,
                "Mental Health": 0.8,
                "Endocrine": 0.7,
                "Respiratory": 0.7
            },
            "Stress": {
                "Mental Health": 0.9,
                "Neurological": 0.8,
                "Endocrine": 0.8,
                "Immune": 0.7,
                "Digestive": 0.7,
                "Cardiovascular": 0.7,
                "Metabolic": 0.6
            },
            "Environmental Toxins": {
                "Immune": 0.8,
                "Respiratory": 0.8,
                "Integumentary": 0.7,
                "Endocrine": 0.7,
                "Neurological": 0.6,
                "Reproductive": 0.6
            }
        }
        
        # Define common disease patterns across multiple systems
        # Format: "Disease Pattern": {"system": involvement_strength, ...}
        self.multi_system_disease_patterns = {
            "Metabolic Syndrome": {
                "Metabolic": 0.9,
                "Cardiovascular": 0.8,
                "Endocrine": 0.8,
                "Immune": 0.6
            },
            "Autoimmune Disorders": {
                "Immune": 0.9,
                "Endocrine": 0.7,
                "Digestive": 0.7,
                "Musculoskeletal": 0.7,
                "Neurological": 0.6,
                "Integumentary": 0.6
            },
            "Chronic Fatigue Syndrome": {
                "Immune": 0.8,
                "Neurological": 0.8,
                "Endocrine": 0.7,
                "Metabolic": 0.7,
                "Mental Health": 0.7
            },
            "Fibromyalgia": {
                "Neurological": 0.8,
                "Musculoskeletal": 0.8,
                "Immune": 0.7,
                "Mental Health": 0.7,
                "Endocrine": 0.6
            },
            "Irritable Bowel Syndrome": {
                "Digestive": 0.9,
                "Neurological": 0.7,
                "Immune": 0.7,
                "Mental Health": 0.7,
                "Endocrine": 0.5
            },
            "Depression": {
                "Mental Health": 0.9,
                "Neurological": 0.8,
                "Endocrine": 0.7,
                "Immune": 0.6,
                "Digestive": 0.5
            },
            "Chronic Inflammation": {
                "Immune": 0.9,
                "Cardiovascular": 0.7,
                "Metabolic": 0.7,
                "Digestive": 0.7,
                "Musculoskeletal": 0.7,
                "Neurological": 0.6
            }
        }
    
    def get_related_systems(self, system, threshold=0.5):
        """
        Get systems related to the given system based on connection strength.
        
        Args:
            system (str): The body system to find related systems for
            threshold (float): Minimum connection strength threshold
            
        Returns:
            list: List of (related_system, connection_strength) tuples
        """
        related = []
        for (sys1, sys2), strength in self.system_connections.items():
            if sys1 == system and strength >= threshold:
                related.append((sys2, strength))
        
        # Sort by connection strength (descending)
        related.sort(key=lambda x: x[1], reverse=True)
        return related
    
    def get_systems_for_symptom(self, symptom, threshold=0.3):
        """
        Get body systems associated with a symptom.
        
        Args:
            symptom (str): The symptom to find associated systems for
            threshold (float): Minimum association strength threshold
            
        Returns:
            list: List of (system, association_strength) tuples
        """
        if symptom not in self.symptom_system_mapping:
            return []
        
        associations = []
        for system, strength in self.symptom_system_mapping[symptom].items():
            if strength >= threshold:
                associations.append((system, strength))
        
        # Sort by association strength (descending)
        associations.sort(key=lambda x: x[1], reverse=True)
        return associations
    
    def get_symptoms_for_system(self, system, threshold=0.5):
        """
        Get symptoms associated with a body system.
        
        Args:
            system (str): The body system to find associated symptoms for
            threshold (float): Minimum association strength threshold
            
        Returns:
            list: List of (symptom, association_strength) tuples
        """
        associations = []
        for symptom, systems in self.symptom_system_mapping.items():
            if system in systems and systems[system] >= threshold:
                associations.append((symptom, systems[system]))
        
        # Sort by association strength (descending)
        associations.sort(key=lambda x: x[1], reverse=True)
        return associations
    
    def get_lifestyle_impact(self, factor, system=None):
        """
        Get the impact of a lifestyle factor on body systems.
        
        Args:
            factor (str): The lifestyle factor
            system (str, optional): Specific system to get impact for
            
        Returns:
            dict or float: Dictionary of system impacts or specific impact value
        """
        if factor not in self.lifestyle_system_impact:
            return {} if system is None else 0.0
        
        if system is None:
            return self.lifestyle_system_impact[factor]
        else:
            return self.lifestyle_system_impact[factor].get(system, 0.0)
    
    def analyze_symptom_pattern(self, symptoms):
        """
        Analyze a pattern of symptoms to identify affected body systems.
        
        Args:
            symptoms (list): List of symptoms
            
        Returns:
            dict: Dictionary of body systems and their involvement scores
        """
        system_scores = defaultdict(float)
        
        # Calculate system involvement based on symptoms
        for symptom in symptoms:
            if symptom in self.symptom_system_mapping:
                for system, strength in self.symptom_system_mapping[symptom].items():
                    system_scores[system] += strength
        
        # Normalize scores
        if system_scores:
            max_score = max(system_scores.values())
            if max_score > 0:
                for system in system_scores:
                    system_scores[system] /= max_score
        
        # Sort systems by score (descending)
        sorted_systems = sorted(system_scores.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_systems)
    
    def identify_multi_system_patterns(self, symptoms, threshold=0.6):
        """
        Identify potential multi-system disease patterns based on symptoms.
        
        Args:
            symptoms (list): List of symptoms
            threshold (float): Minimum match score threshold
            
        Returns:
            list: List of (pattern_name, match_score) tuples
        """
        # First analyze which systems are involved based on symptoms
        system_involvement = self.analyze_symptom_pattern(symptoms)
        
        # Calculate match scores for each multi-system disease pattern
        pattern_scores = {}
        for pattern, pattern_systems in self.multi_system_disease_patterns.items():
            score = 0.0
            total_weight = 0.0
            
            for system, pattern_weight in pattern_systems.items():
                system_score = system_involvement.get(system, 0.0)
                score += system_score * pattern_weight
                total_weight += pattern_weight
            
            if total_weight > 0:
                pattern_scores[pattern] = score / total_weight
        
        # Filter and sort patterns by score
        matched_patterns = [(pattern, score) for pattern, score in pattern_scores.items() if score >= threshold]
        matched_patterns.sort(key=lambda x: x[1], reverse=True)
        
        return matched_patterns
    
    def suggest_related_questions(self, symptoms, asked_symptoms=None):
        """
        Suggest related questions to ask based on symptoms already reported.
        
        Args:
            symptoms (list): List of symptoms already reported
            asked_symptoms (list, optional): List of symptoms already asked about
            
        Returns:
            list: List of suggested symptoms to ask about next
        """
        if asked_symptoms is None:
            asked_symptoms = []
        
        # Combine reported and asked symptoms to avoid suggesting them again
        excluded_symptoms = set(symptoms + asked_symptoms)
        
        # Identify affected systems based on reported symptoms
        system_involvement = self.analyze_symptom_pattern(symptoms)
        top_systems = sorted(system_involvement.items(), key=lambda x: x[1], reverse=True)
        
        # Get related systems for the top affected systems
        related_systems = []
        for system, score in top_systems[:3]:  # Consider top 3 systems
            related = self.get_related_systems(system)
            related_systems.extend(related)
        
        # Get symptoms associated with top and related systems
        potential_symptoms = []
        
        # Add symptoms from top affected systems
        for system, score in top_systems[:3]:
            system_symptoms = self.get_symptoms_for_system(system)
            for symptom, strength in system_symptoms:
                if symptom not in excluded_symptoms:
                    potential_symptoms.append((symptom, strength * score))
        
        # Add symptoms from related systems
        for system, connection_strength in related_systems:
            system_score = system_involvement.get(system, 0.3)  # Default to low score if not already involved
            system_symptoms = self.get_symptoms_for_system(system)
            for symptom, strength in system_symptoms:
                if symptom not in excluded_symptoms:
                    # Adjust strength based on connection strength and system involvement
                    adjusted_strength = strength * connection_strength * (system_score + 0.5)
                    potential_symptoms.append((symptom, adjusted_strength))
        
        # Combine duplicate symptoms by taking the maximum score
        symptom_scores = {}
        for symptom, score in potential_symptoms:
            symptom_scores[symptom] = max(score, symptom_scores.get(symptom, 0.0))
        
        # Sort by score and return top symptoms
        suggested_symptoms = sorted(symptom_scores.items(), key=lambda x: x[1], reverse=True)
        return [symptom for symptom, _ in suggested_symptoms[:5]]  # Return top 5 symptoms
    
    def explain_symptom_connections(self, symptoms):
        """
        Explain the connections between symptoms across different body systems.
        
        Args:
            symptoms (list): List of symptoms
            
        Returns:
            dict: Dictionary with explanation of connections
        """
        if not symptoms:
            return {"explanation": "No symptoms provided to analyze."}
        
        # Analyze system involvement
        system_involvement = self.analyze_symptom_pattern(symptoms)
        top_systems = sorted(system_involvement.items(), key=lambda x: x[1], reverse=True)
        
        # Map each symptom to its systems
        symptom_systems = {}
        for symptom in symptoms:
            if symptom in self.symptom_system_mapping:
                symptom_systems[symptom] = sorted(
                    self.symptom_system_mapping[symptom].items(),
                    key=lambda x: x[1],
                    reverse=True
                )
        
        # Find connections between symptoms through shared systems
        symptom_connections = []
        for i, symptom1 in enumerate(symptoms):
            for symptom2 in symptoms[i+1:]:
                if symptom1 in self.symptom_system_mapping and symptom2 in self.symptom_system_mapping:
                    shared_systems = set(self.symptom_system_mapping[symptom1].keys()) & set(self.symptom_system_mapping[symptom2].keys())
                    if shared_systems:
                        # Calculate connection strength based on shared systems
                        connection_strength = 0.0
                        for system in shared_systems:
                            strength1 = self.symptom_system_mapping[symptom1][system]
                            strength2 = self.symptom_system_mapping[symptom2][system]
                            connection_strength += (strength1 * strength2)
                        
                        connection_strength /= len(shared_systems)
                        
                        symptom_connections.append({
                            "symptom1": symptom1,
                            "symptom2": symptom2,
                            "shared_systems": list(shared_systems),
                            "connection_strength": connection_strength
                        })
        
        # Sort connections by strength
        symptom_connections.sort(key=lambda x: x["connection_strength"], reverse=True)
        
        # Identify potential multi-system patterns
        potential_patterns = self.identify_multi_system_patterns(symptoms)
        
        # Generate explanation
        explanation = {
            "affected_systems": [{"system": system, "involvement": score} for system, score in top_systems],
            "symptom_systems": symptom_systems,
            "symptom_connections": symptom_connections,
            "potential_patterns": potential_patterns,
            "summary": self._generate_connection_summary(symptoms, top_systems, symptom_connections, potential_patterns)
        }
        
        return explanation
    
    def _generate_connection_summary(self, symptoms, top_systems, symptom_connections, potential_patterns):
        """Generate a human-readable summary of symptom connections."""
        if not symptoms:
            return "No symptoms provided to analyze."
        
        summary = []
        
        # Summarize affected systems
        if top_systems:
            systems_text = ", ".join([f"{system} ({score:.2f})" for system, score in top_systems[:3]])
            summary.append(f"Your symptoms primarily affect these body systems: {systems_text}.")
        
        # Summarize key connections
        if symptom_connections:
            top_connections = symptom_connections[:3]  # Top 3 connections
            connection_texts = []
            for conn in top_connections:
                shared = ", ".join(conn["shared_systems"][:2])  # Top 2 shared systems
                connection_texts.append(f"{conn['symptom1']} and {conn['symptom2']} are connected through the {shared} systems")
            
            if connection_texts:
                summary.append("Key connections between your symptoms: " + "; ".join(connection_texts) + ".")
        
        # Summarize potential patterns
        if potential_patterns:
            patterns_text = ", ".join([f"{pattern} ({score:.2f})" for pattern, score in potential_patterns[:2]])
            summary.append(f"Your symptoms may be related to these patterns: {patterns_text}.")
        
        # Add integrative perspective
        summary.append("From an integrative medicine perspective, these symptoms suggest interactions between multiple body systems that should be addressed holistically rather than in isolation.")
        
        return " ".join(summary)
    
    def suggest_lifestyle_interventions(self, affected_systems):
        """
        Suggest lifestyle interventions based on affected body systems.
        
        Args:
            affected_systems (dict): Dictionary of affected systems and their scores
            
        Returns:
            dict: Dictionary of suggested interventions by category
        """
        interventions = {
            "Diet": [],
            "Sleep": [],
            "Exercise": [],
            "Stress Management": [],
            "Environmental": []
        }
        
        # Diet interventions
        if "Digestive" in affected_systems or "Immune" in affected_systems or "Metabolic" in affected_systems:
            interventions["Diet"].append("Consider an anti-inflammatory diet rich in whole foods, vegetables, and omega-3 fatty acids")
            interventions["Diet"].append("Identify and eliminate potential food sensitivities")
            interventions["Diet"].append("Ensure adequate fiber intake to support gut microbiome health")
        
        if "Endocrine" in affected_systems or "Metabolic" in affected_systems:
            interventions["Diet"].append("Balance blood sugar by reducing refined carbohydrates and increasing protein and healthy fats")
            interventions["Diet"].append("Consider intermittent fasting if appropriate for your condition")
        
        if "Cardiovascular" in affected_systems:
            interventions["Diet"].append("Reduce sodium intake and increase potassium-rich foods")
            interventions["Diet"].append("Include heart-healthy fats like olive oil and avocados")
        
        if "Neurological" in affected_systems or "Mental Health" in affected_systems:
            interventions["Diet"].append("Increase intake of omega-3 fatty acids and antioxidant-rich foods")
            interventions["Diet"].append("Consider Mediterranean diet pattern which supports brain health")
        
        # Sleep interventions
        if "Neurological" in affected_systems or "Endocrine" in affected_systems or "Mental Health" in affected_systems:
            interventions["Sleep"].append("Establish a consistent sleep schedule with regular sleep and wake times")
            interventions["Sleep"].append("Create a relaxing bedtime routine to signal the body it's time to sleep")
            interventions["Sleep"].append("Optimize sleep environment: dark, quiet, cool room")
        
        if "Respiratory" in affected_systems or "Cardiovascular" in affected_systems:
            interventions["Sleep"].append("Consider evaluation for sleep apnea if you have symptoms like snoring or daytime fatigue")
            interventions["Sleep"].append("Elevate head of bed if you experience nighttime breathing difficulties")
        
        # Exercise interventions
        if "Musculoskeletal" in affected_systems or "Metabolic" in affected_systems:
            interventions["Exercise"].append("Incorporate strength training 2-3 times per week to support muscle and bone health")
            interventions["Exercise"].append("Include flexibility exercises like stretching or yoga to improve joint mobility")
        
        if "Cardiovascular" in affected_systems or "Respiratory" in affected_systems:
            interventions["Exercise"].append("Aim for 150 minutes of moderate aerobic activity weekly")
            interventions["Exercise"].append("Consider interval training for cardiovascular health if appropriate for your fitness level")
        
        if "Mental Health" in affected_systems or "Neurological" in affected_systems:
            interventions["Exercise"].append("Include daily movement for mood regulation and cognitive benefits")
            interventions["Exercise"].append("Consider mind-body exercises like tai chi or yoga")
        
        # Stress management interventions
        if "Mental Health" in affected_systems or "Neurological" in affected_systems or "Endocrine" in affected_systems:
            interventions["Stress Management"].append("Practice daily mindfulness meditation or deep breathing exercises")
            interventions["Stress Management"].append("Consider cognitive behavioral techniques to manage stress responses")
            interventions["Stress Management"].append("Establish healthy boundaries in work and personal life")
        
        if "Digestive" in affected_systems or "Immune" in affected_systems:
            interventions["Stress Management"].append("Practice relaxation techniques before meals to support digestion")
            interventions["Stress Management"].append("Consider gut-directed hypnotherapy for digestive symptoms exacerbated by stress")
        
        if "Cardiovascular" in affected_systems:
            interventions["Stress Management"].append("Monitor stress effects on blood pressure and heart rate")
            interventions["Stress Management"].append("Practice heart rate variability biofeedback techniques")
        
        # Environmental interventions
        if "Respiratory" in affected_systems or "Immune" in affected_systems or "Integumentary" in affected_systems:
            interventions["Environmental"].append("Minimize exposure to environmental allergens and toxins")
            interventions["Environmental"].append("Consider air purification in home and work environments")
            interventions["Environmental"].append("Use non-toxic personal care and cleaning products")
        
        if "Neurological" in affected_systems or "Endocrine" in affected_systems:
            interventions["Environmental"].append("Reduce exposure to endocrine-disrupting chemicals in food containers and products")
            interventions["Environmental"].append("Create a low-EMF sleep environment by removing electronics from bedroom")
        
        # Remove empty categories
        for category in list(interventions.keys()):
            if not interventions[category]:
                del interventions[category]
        
        return interventions
    
    def generate_holistic_assessment(self, symptoms, lifestyle_factors=None):
        """
        Generate a holistic health assessment based on symptoms and lifestyle factors.
        
        Args:
            symptoms (list): List of symptoms
            lifestyle_factors (dict, optional): Dictionary of lifestyle factors and their values
            
        Returns:
            dict: Holistic assessment including affected systems, connections, and recommendations
        """
        if not symptoms:
            return {"assessment": "No symptoms provided for assessment."}
        
        # Analyze symptom pattern
        system_involvement = self.analyze_symptom_pattern(symptoms)
        
        # Explain symptom connections
        connections = self.explain_symptom_connections(symptoms)
        
        # Identify potential multi-system patterns
        patterns = self.identify_multi_system_patterns(symptoms)
        
        # Suggest lifestyle interventions
        interventions = self.suggest_lifestyle_interventions(system_involvement)
        
        # Suggest related questions to ask
        suggested_questions = self.suggest_related_questions(symptoms)
        
        # Generate holistic assessment
        assessment = {
            "affected_systems": system_involvement,
            "symptom_connections": connections,
            "potential_patterns": patterns,
            "lifestyle_interventions": interventions,
            "suggested_questions": suggested_questions,
            "summary": self._generate_holistic_summary(system_involvement, connections, patterns, interventions)
        }
        
        return assessment
    
    def _generate_holistic_summary(self, system_involvement, connections, patterns, interventions):
        """Generate a human-readable summary of the holistic assessment."""
        summary = []
        
        # Summarize affected systems
        top_systems = sorted(system_involvement.items(), key=lambda x: x[1], reverse=True)[:3]
        if top_systems:
            systems_text = ", ".join([system for system, _ in top_systems])
            summary.append(f"Your health concerns primarily involve the {systems_text} systems.")
        
        # Summarize key connections
        if "summary" in connections:
            summary.append(connections["summary"])
        
        # Summarize potential patterns
        if patterns:
            top_patterns = patterns[:2]
            patterns_text = ", ".join([pattern for pattern, _ in top_patterns])
            summary.append(f"Your symptoms suggest patterns consistent with {patterns_text}.")
        
        # Summarize key interventions
        if interventions:
            summary.append("A holistic approach to your health would include:")
            for category, items in interventions.items():
                if items:
                    summary.append(f"- {category}: {items[0]}")
        
        # Add integrative medicine perspective
        summary.append("From an integrative medicine perspective, addressing the interconnections between these systems is essential for resolving your health concerns. This requires a unified approach rather than treating each symptom in isolation.")
        
        return " ".join(summary)

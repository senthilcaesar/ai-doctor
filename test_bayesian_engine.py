"""
Test script for the Bayesian diagnosis engine.
This script demonstrates how the Bayesian engine updates its beliefs based on observed symptoms.
"""

import sys
import os
from bayesian_engine import BayesianDiagnosisEngine

def test_bayesian_engine():
    """Test the Bayesian diagnosis engine with a simple scenario."""
    print("Initializing Bayesian diagnosis engine...")
    engine = BayesianDiagnosisEngine()
    
    # Print initial beliefs
    print("\nInitial beliefs (prior probabilities):")
    for disease, prob in sorted(engine.beliefs.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {disease}: {prob:.4f}")
    
    # Scenario: A patient with flu-like symptoms
    print("\nScenario: A patient with flu-like symptoms")
    
    # Observe fever
    print("\nObserving symptom: Fever (present)")
    engine.update_belief("Fever", True)
    
    # Print updated beliefs
    print("\nUpdated beliefs after observing fever:")
    for disease, prob in sorted(engine.beliefs.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {disease}: {prob:.4f}")
    
    # Observe cough
    print("\nObserving symptom: Cough (present)")
    engine.update_belief("Cough", True)
    
    # Print updated beliefs
    print("\nUpdated beliefs after observing cough:")
    for disease, prob in sorted(engine.beliefs.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {disease}: {prob:.4f}")
    
    # Observe fatigue
    print("\nObserving symptom: Fatigue (present)")
    engine.update_belief("Fatigue", True)
    
    # Print updated beliefs
    print("\nUpdated beliefs after observing fatigue:")
    for disease, prob in sorted(engine.beliefs.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {disease}: {prob:.4f}")
    
    # Observe runny nose
    print("\nObserving symptom: Runny Nose (present)")
    engine.update_belief("Runny Nose", True)
    
    # Print updated beliefs
    print("\nUpdated beliefs after observing runny nose:")
    for disease, prob in sorted(engine.beliefs.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {disease}: {prob:.4f}")
    
    # Observe no shortness of breath
    print("\nObserving symptom: Shortness of Breath (absent)")
    engine.update_belief("Shortness of Breath", False)
    
    # Print updated beliefs
    print("\nUpdated beliefs after observing no shortness of breath:")
    for disease, prob in sorted(engine.beliefs.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {disease}: {prob:.4f}")
    
    # Get the top diagnoses
    print("\nTop diagnoses:")
    for disease, prob in engine.get_top_diagnoses(3):
        print(f"  {disease}: {prob:.4f}")
    
    # Get the next questions to ask
    print("\nSuggested next questions:")
    for symptom, info_gain in engine.suggest_questions(3):
        print(f"  {symptom} (Information Gain: {info_gain:.4f})")
    
    # Get a detailed explanation of the top diagnosis
    top_diagnosis = engine.get_top_diagnoses(1)[0][0]
    print(f"\nDetailed explanation for {top_diagnosis}:")
    explanation = engine.explain_reasoning(top_diagnosis)
    print(f"  {explanation['explanation']}")
    
    # Print the supporting evidence
    print("\nSupporting evidence:")
    for factor in explanation['evidence_factors'][:3]:
        symptom_status = "Presence" if factor['present'] else "Absence"
        effect = factor['effect'].capitalize()
        strength = factor['strength'].capitalize()
        print(f"  {symptom_status} of {factor['symptom']}: {strength} {effect} factor (Likelihood: {factor['likelihood_factor']:.2f})")
    
    # Get a differential diagnosis
    print("\nDifferential diagnosis:")
    differential = engine.get_differential_diagnosis(3)
    for diagnosis in differential:
        print(f"  {diagnosis['disease']} (Probability: {diagnosis['probability']:.4f})")
        if diagnosis['supporting_evidence']:
            print("    Supporting evidence:")
            for evidence in diagnosis['supporting_evidence'][:2]:
                print(f"      {evidence['symptom']} ({evidence['strength']} support, p={evidence['probability']:.2f})")
        if diagnosis['contradicting_evidence']:
            print("    Contradicting evidence:")
            for evidence in diagnosis['contradicting_evidence'][:2]:
                print(f"      {evidence['symptom']} ({evidence['strength']} contradiction, p={evidence['probability']:.2f})")
    
    # Reset the engine
    print("\nResetting the engine...")
    engine.reset()
    
    # Print beliefs after reset
    print("\nBeliefs after reset (should be back to prior probabilities):")
    for disease, prob in sorted(engine.beliefs.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {disease}: {prob:.4f}")

if __name__ == "__main__":
    test_bayesian_engine()

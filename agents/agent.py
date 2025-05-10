class Agent:
    def __init__(self, name, instructions, model="gpt-4.1-2025-04-14"):
        """
        Initialize an Agent instance.
        
        Args:
            name (str): The name of the agent
            instructions (str): The instructions for the agent
            model (str): The model to use for the agent
        """
        self.name = name
        self.instructions = instructions
        self.model = model
    
    def calculate_bmi(self, height, weight, height_unit="cm", weight_unit="kg"):
        """
        Calculate BMI and provide health assessment.
        
        Args:
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
        # Convert height to meters
        height_m = height / 100.0 if height_unit == "cm" else height * 0.3048
        
        # Convert weight to kg
        weight_kg = weight if weight_unit == "kg" else weight * 0.45359237
        
        # Calculate BMI
        bmi = weight_kg / (height_m ** 2)
        
        # Determine BMI category
        if bmi < 18.5:
            category = "Underweight"
            assessment = "Your BMI indicates you are underweight. This might suggest insufficient caloric intake or other health issues."
            recommendations = "Consider consulting with a healthcare provider about healthy weight gain strategies. Focus on nutrient-dense foods and possibly increase your caloric intake."
        elif 18.5 <= bmi < 25:
            category = "Normal weight"
            assessment = "Your BMI is within the normal range, which is associated with good health outcomes."
            recommendations = "Maintain your current healthy habits. Continue with regular physical activity and a balanced diet."
        elif 25 <= bmi < 30:
            category = "Overweight"
            assessment = "Your BMI indicates you are overweight, which may increase the risk of certain health conditions."
            recommendations = "Consider moderate lifestyle changes such as increased physical activity and dietary adjustments. Consult with a healthcare provider for personalized advice."
        else:
            category = "Obese"
            assessment = "Your BMI indicates obesity, which is associated with higher risks for various health conditions including heart disease, diabetes, and certain cancers."
            recommendations = "It's recommended to consult with healthcare providers for a comprehensive health assessment and to discuss potential weight management strategies."
        
        return {
            "bmi_value": round(bmi, 1),
            "bmi_category": category,
            "health_assessment": assessment,
            "recommendations": recommendations
        }
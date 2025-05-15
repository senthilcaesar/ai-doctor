# Virtual Doctor Assistant

![Virtual Doctor Assistant](https://img.shields.io/badge/Virtual%20Doctor-Assistant-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0-FF4B4B)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-00A67E)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB)

A futuristic, AI inspired virtual doctor assistant application built with Streamlit and powered by OpenAI's GPT models. This application simulates a virtual doctor that collects patient health information through an interactive form and allows patients to discuss their health concerns with an AI assistant.

![app_logic](images/app_logic.png)

## Live Demo

The application is live at: **[https://ai-doctor-v1.streamlit.app/](https://ai-doctor-v1.streamlit.app/)**

This Virtual Doctor Assistant helps users assess their health by collecting patient information through an interactive form and providing personalized health insights. It calculates BMI based on height and weight, offers health recommendations, and enables users to discuss their health concerns through an AI-powered chat interface. The assistant analyzes symptoms, provides general health guidance, and creates a seamless, futuristic healthcare experience—all while maintaining that this is for demonstration purposes only and not a replacement for professional medical advice.

## Technologies Used

- **Frontend**: Streamlit
- **Backend**: Python
- **AI**: OpenAI API (GPT-4o, GPT-4-turbo, GPT-3.5-turbo)
- **AI Framework**: OpenAI Agents Python library
- **Data Handling**: Pandas
- **Web Search**: SerpAPI for medical information retrieval
- **Styling**: Custom CSS

## Prerequisites

- Python 3.9 or higher
- OpenAI API key
- SERP API key (for medical information retrieval)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/virtual-doctor-assistant.git
   cd virtual-doctor-assistant
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the setup script to configure the SERP API integration:

   ```bash
   python setup_serp_api.py
   ```

   This script will:

   - Check if the required packages are installed
   - Create a `.streamlit/secrets.toml` file if it doesn't exist
   - Guide you through adding your API keys
   - Test the SERP API integration

   Alternatively, you can manually create a `.streamlit/secrets.toml` file with your API keys:

   ```toml
   # OpenAI API key for the main assistant functionality
   OPENAI_API_KEY = "your-openai-api-key-here"

   # SERP API key for medical information retrieval
   # Get your key at: https://serpapi.com/
   SERP_API_KEY = "your-serp-api-key-here"
   ```

## Usage

1. Run the Streamlit application:

   ```bash
   streamlit run app.py
   ```

2. Open your browser and navigate to the URL displayed in the terminal (usually http://localhost:8501)

3. Fill out the patient information form:

   - Navigate through the tabs to provide your information
   - Required fields are in the Basic Info and Symptoms tabs
   - Enter your height and weight to receive a BMI assessment
   - Review your information in the Submit Information tab
   - Click "Submit Information" to proceed

4. Chat with the virtual doctor:
   - After submitting your information, click on the "Virtual Doctor" button in the sidebar
   - The virtual doctor will acknowledge your BMI assessment and provide health recommendations
   - Type your messages in the chat input field
   - Receive responses from the AI-powered virtual doctor

## 📁 Project Structure

```
virtual-doctor-assistant/
├── app.py                    # Main application file
├── ui.py                     # UI components and styling
├── serp_service.py           # SERP API service for medical information retrieval
├── serp_utils.py             # Utility functions for SERP API integration
├── setup_serp_api.py         # Setup script for SERP API integration
├── test_serp_api.py          # Test script for SERP API integration
├── feedback_utils.py         # Feedback collection and analysis utilities
├── feedback_dashboard.py     # Feedback visualization dashboard
├── SERP_API_INTEGRATION.md   # Documentation for SERP API integration
├── .streamlit/               # Streamlit configuration
│   └── secrets.toml          # API keys and secrets
├── feedback/                 # Feedback data storage directory
│   └── user_feedback.csv     # Feedback data in CSV format
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation
```

## Implementation Details

### Architecture

The application follows a modular architecture with separation of concerns:

- **app.py**: Contains the main application logic, session state management, and API calls
- **ui.py**: Contains all UI components, styling, and rendering functions

### AI Integration

The application uses OpenAI's GPT models and Agents framework to power the virtual doctor assistant:

- System instructions define the assistant's role and limitations
- Patient information including BMI assessment is added to the conversation context
- The assistant maintains a conversational history for context-aware responses
- Specialized agents handle specific tasks like BMI calculation

### SERP API Integration

The application integrates with SERP API to provide up-to-date medical information:

- **Medical Information Retrieval**: Enhances responses with current medical information from reputable sources
- **Intelligent Enhancement**: Automatically determines when to supplement responses with web search results
- **Source Validation**: Prioritizes trusted medical sources like Mayo Clinic, NIH, CDC, and WHO
- **Medical Disclaimers**: Includes appropriate disclaimers with information from web searches
- **Rate Limiting and Caching**: Implements rate limiting and caching to optimize API usage

For detailed information about the SERP API integration, see [SERP_API_INTEGRATION.md](SERP_API_INTEGRATION.md).

### Feedback System

The application includes a comprehensive feedback collection and analysis system:

- **Feedback Collection**: Users can provide feedback at the end of their session by clicking the "End Session & Provide Feedback" button
- **Rating System**: Users can rate their experience on a scale of 1-5 stars across multiple dimensions:
  - Overall satisfaction
  - Helpfulness of responses
  - Clarity of information
  - Empathy and bedside manner
  - Perceived accuracy of information
- **Comments**: Users can provide qualitative feedback through an open text field
- **Data Storage**: Feedback is stored in a CSV file for persistence and easy analysis
- **Feedback Dashboard**: A dedicated dashboard visualizes feedback data with:
  - Key statistics (total submissions, average ratings, positive feedback rate)
  - Rating breakdowns by category
  - Distribution of overall ratings
  - Common themes extracted from comments
  - Recent feedback entries
  - Data export functionality

To view the feedback dashboard:

```bash
streamlit run feedback_dashboard.py
```

## Future Improvements

- Add authentication for patient privacy
- Implement data encryption for sensitive information
- Add support for file uploads (medical records, images)
- ✅ Integrate with medical databases for more accurate responses (Implemented via SERP API)
- Add multilingual support
- Implement voice input/output capabilities
- Create a mobile-friendly version
- Expand health metrics beyond BMI (blood pressure, cholesterol, etc.)
- Enhance the feedback system:
  - Implement sentiment analysis on feedback comments
  - Add automated alerts for negative feedback
  - Create an admin dashboard for feedback management
  - Develop a feedback-driven model selection system
  - Implement A/B testing for different conversation approaches

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Areas for Improvement

### 1. Evaluation and Feedback Mechanisms

- No built-in way to evaluate the quality of the agent's responses
- Lacks metrics for measuring conversation effectiveness or patient satisfaction
- Could benefit from a feedback system to improve responses over time

### 2. Diagnostic Limitations

- Limited ability to process complex symptom combinations
- ✅ Integration with medical knowledge databases via SERP API for more accurate assessments
- Lacks structured differential diagnosis capabilities

### 3. Personalization Enhancements

- Could better tailor responses based on patient demographics and history
- Limited ability to remember and reference previous conversations with the same patient
- Could improve adaptation to different communication styles and preferences

### 4. Medical Context Expansion

- ✅ Integration with external medical resources through SERP API
- ✅ Enhanced ability to provide evidence-based recommendations from trusted sources
- Could benefit from more specialized knowledge in different medical domains

### 5. Technical Improvements

- No built-in analytics to track usage patterns and common health concerns
- Limited ability to handle multimedia inputs (like images of symptoms)
- Could implement more sophisticated NLP techniques for symptom extraction

### 6. User Experience Refinements

- No voice input/output capabilities for accessibility
- Limited multilingual support
- Could improve the transition between information collection and conversation

## Recommendations for Enhancement

1. **Implement a feedback system** to collect user ratings and comments after each session
2. ✅ **Integrate with medical knowledge databases** - Implemented via SERP API integration
3. **Add analytics tracking** to identify common concerns and improve responses over time
4. **Develop specialized modules** for different medical domains (cardiology, dermatology, etc.)
5. **Implement a structured evaluation framework** to assess response quality
6. **Add multimedia capabilities** for patients to share images of visible symptoms
7. **Enhance personalization** by developing patient profiles that persist across sessions
8. **Implement voice interfaces** for improved accessibility

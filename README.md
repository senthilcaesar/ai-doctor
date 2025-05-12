# Virtual Doctor Assistant

![Virtual Doctor Assistant](https://img.shields.io/badge/Virtual%20Doctor-Assistant-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0-FF4B4B)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-00A67E)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB)

A futuristic, AI inspired virtual doctor assistant application built with Streamlit and powered by OpenAI's GPT models. This application simulates a virtual doctor that collects patient health information through an interactive form and allows patients to discuss their health concerns with an AI assistant.

## Live Demo

The application is live at: **[https://ai-doctor-v1.streamlit.app/](https://ai-doctor-v1.streamlit.app/)**

This Virtual Doctor Assistant helps users assess their health by collecting patient information through an interactive form and providing personalized health insights. It calculates BMI based on height and weight, offers health recommendations, and enables users to discuss their health concerns through an AI-powered chat interface. The assistant analyzes symptoms, provides general health guidance, and creates a seamless, futuristic healthcare experience—all while maintaining that this is for demonstration purposes only and not a replacement for professional medical advice.

## Technologies Used

- **Frontend**: Streamlit
- **Backend**: Python
- **AI**: OpenAI API (GPT-4o, GPT-4-turbo, GPT-3.5-turbo)
- **AI Framework**: OpenAI Agents Python library
- **Data Handling**: Pandas
- **Styling**: Custom CSS

## Prerequisites

- Python 3.9 or higher
- OpenAI API key

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

4. Create a `.streamlit/secrets.toml` file with your OpenAI API key:
   ```toml
   OPENAI_API_KEY = "your-api-key-here"
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
├── app.py                 # Main application file
├── ui.py                  # UI components and styling
├── .streamlit/            # Streamlit configuration
│   └── secrets.toml       # API keys and secrets
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
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

## Future Improvements

- Add authentication for patient privacy
- Implement data encryption for sensitive information
- Add support for file uploads (medical records, images)
- Integrate with medical databases for more accurate responses
- Add multilingual support
- Implement voice input/output capabilities
- Create a mobile-friendly version
- Expand health metrics beyond BMI (blood pressure, cholesterol, etc.)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

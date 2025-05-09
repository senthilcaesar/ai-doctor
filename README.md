# Virtual Doctor Assistant

![Virtual Doctor Assistant](https://img.shields.io/badge/Virtual%20Doctor-Assistant-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0-FF4B4B)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-00A67E)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB)

A futuristic, sci-fi inspired virtual doctor assistant application built with Streamlit and powered by OpenAI's GPT models. This application simulates a virtual doctor that collects patient health information through an interactive form and allows patients to discuss their health concerns with an AI assistant.

> **Note:** This application does not provide medical advice or diagnosis. It is for demonstration purposes only.

## 🌟 Features

- **Patient Information Intake Form**

  - Collect comprehensive patient information across multiple categories
  - Validate required fields and provide visual feedback
  - Review all information before submission

- **Virtual Doctor Chat**

  - Discuss health concerns with an AI-powered virtual doctor
  - Context-aware conversations based on submitted patient information
  - Support for multiple OpenAI models (GPT-4o, GPT-4-turbo, GPT-3.5-turbo)

- **User Interface**
  - Intuitive navigation between data input and virtual doctor chat
  - Futuristic sci-fi inspired design with custom styling
  - Responsive layout that works on various screen sizes
  - Table-based information display for better readability

## 🛠️ Technologies Used

- **Frontend**: Streamlit
- **Backend**: Python
- **AI**: OpenAI API (GPT-4o, GPT-4-turbo, GPT-3.5-turbo)
- **Data Handling**: Pandas
- **Styling**: Custom CSS

## 📋 Prerequisites

- Python 3.9 or higher
- OpenAI API key

## 🚀 Installation

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

## 🏃‍♂️ Usage

1. Run the Streamlit application:

   ```bash
   streamlit run app.py
   ```

2. Open your browser and navigate to the URL displayed in the terminal (usually http://localhost:8501)

3. Fill out the patient information form:

   - Navigate through the tabs to provide your information
   - Required fields are in the Basic Info and Symptoms tabs
   - Review your information in the Submit Information tab
   - Click "Submit Information" to proceed

4. Chat with the virtual doctor:
   - After submitting your information, click on the "Virtual Doctor" button in the sidebar
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

## 🔍 Implementation Details

### Architecture

The application follows a modular architecture with separation of concerns:

- **app.py**: Contains the main application logic, session state management, and API calls
- **ui.py**: Contains all UI components, styling, and rendering functions

### Key Components

1. **Patient Information Form**

   - Multi-tab interface for collecting different categories of information
   - Form validation to ensure required fields are filled
   - Custom HTML tables for displaying information in the review section

2. **Navigation System**

   - Sidebar navigation with "Input Data" and "Virtual Doctor" buttons
   - Visual indicators for the active view
   - Conditional enabling of the Virtual Doctor button

3. **Chat Interface**

   - Integration with OpenAI's API for generating responses
   - Context-aware conversations using the patient's information
   - Enhanced chat UI with larger message display area

4. **Session State Management**
   - Persistent storage of patient information
   - Conversation history tracking
   - View state management

### AI Integration

The application uses OpenAI's GPT models to power the virtual doctor assistant:

- System instructions define the assistant's role and limitations
- Patient information is added to the conversation context
- The assistant maintains a conversational history for context-aware responses

## 🔮 Future Improvements

- Add authentication for patient privacy
- Implement data encryption for sensitive information
- Add support for file uploads (medical records, images)
- Integrate with medical databases for more accurate responses
- Add multilingual support
- Implement voice input/output capabilities
- Create a mobile-friendly version

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [Streamlit](https://streamlit.io/) for the amazing web framework
- [OpenAI](https://openai.com/) for the powerful language models
- [Pandas](https://pandas.pydata.org/) for data handling

---

<p align="center">
  Made with ❤️ for a healthier future
</p>

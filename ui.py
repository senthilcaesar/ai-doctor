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
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Rajdhani:wght@300;400;500;600;700&family=Share+Tech+Mono&display=swap');
        
        /* Force light mode */
        :root {
            color-scheme: light only !important;
        }
        
        /* Force light mode for all elements */
        html, body, div, span, applet, object, iframe, h1, h2, h3, h4, h5, h6, p, blockquote, pre, a, abbr, acronym, address, big, cite, code, del, dfn, em, img, ins, kbd, q, s, samp, small, strike, strong, sub, sup, tt, var, b, u, i, center, dl, dt, dd, ol, ul, li, fieldset, form, label, legend, table, caption, tbody, tfoot, thead, tr, th, td, article, aside, canvas, details, embed, figure, figcaption, footer, header, hgroup, menu, nav, output, ruby, section, summary, time, mark, audio, video {
            color-scheme: light only !important;
        }
        
        /* Force light mode for Streamlit elements */
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stSidebar"], [data-testid="stSidebarContent"], .main, .block-container, [data-testid="stVerticalBlock"], [data-testid="stHorizontalBlock"] {
            color-scheme: light only !important;
        }
        
        /* Theme colors */
        :root {
            /* Light theme color palette */
            --primary-color: #00003c;  /* Dark navy blue */
            --primary-light: #0000a0;  /* Lighter navy blue */
            --primary-dark: #000020;  /* Darker navy blue */
            --accent-color: #7B42F6;  /* Neon purple */
            --accent-hover: #9668FA;  /* Lighter neon purple */
            --warning-color: #FFD600;  /* Neon yellow */
            --success-color: #00FF94;  /* Neon green */
            --info-color: #00003c;  /* Dark navy blue */
            --error-color: #FF3D71;  /* Neon red */
            
            /* Text colors */
            --text-color: #333333;  /* Dark gray for text */
            --text-muted: #666666;  /* Medium gray for muted text */
            --text-light: #999999;  /* Light gray for light text */
            
            /* Background colors */
            --bg-primary: #FFFFFF;  /* White background */
            --bg-secondary: #F0F0F0;  /* Light gray background */
            --card-bg: #FFFFFF;  /* White card background */
            
            /* UI elements */
            --border-radius: 16px;
            --border-radius-lg: 24px;
            --border-radius-sm: 12px;
            --border-radius-full: 9999px;
            
            /* Glows and shadows */
            --neon-glow-cyan: 0 0 5px rgba(0, 0, 60, 0.3), 0 0 10px rgba(0, 0, 60, 0.2);
            --neon-glow-cyan-intense: 0 0 10px rgba(0, 0, 60, 0.5), 0 0 15px rgba(0, 0, 60, 0.3);
            --neon-glow-magenta: 0 0 5px rgba(255, 0, 228, 0.3), 0 0 10px rgba(255, 0, 228, 0.2);
            --neon-glow-magenta-intense: 0 0 10px rgba(255, 0, 228, 0.5), 0 0 15px rgba(255, 0, 228, 0.3);
            --neon-glow-purple: 0 0 5px rgba(123, 66, 246, 0.3), 0 0 10px rgba(123, 66, 246, 0.2);
            --neon-glow-yellow: 0 0 5px rgba(255, 214, 0, 0.3), 0 0 10px rgba(255, 214, 0, 0.2);
            --neon-glow-green: 0 0 5px rgba(0, 255, 148, 0.3), 0 0 10px rgba(0, 255, 148, 0.2);
            
            --box-shadow: 0 2px 10px -2px rgba(0, 0, 0, 0.05);
            --box-shadow-hover: 0 4px 15px -2px rgba(0, 0, 0, 0.1);
            --box-shadow-md: 0 4px 15px -3px rgba(0, 0, 0, 0.07);
            --box-shadow-lg: 0 8px 25px -5px rgba(0, 0, 0, 0.08);
            
            /* Sidebar specific */
            --sidebar-bg: #F0F0F0;
            --sidebar-element-bg: #FFFFFF;
            --sidebar-element-active-bg: linear-gradient(135deg, #64B5F6, #42A5F5);
            --sidebar-element-active-color: #FFFFFF;
            --sidebar-element-color: #333333;
            --sidebar-text-color: #333333;
            --sidebar-accent-color: #0066CC;
            
            /* Transitions */
            --transition-speed: 0.3s;
        }
        
        /* Typography - Futuristic sci-fi fonts */
        body {
            font-family: 'Rajdhani', sans-serif;
            color: var(--text-color);
            line-height: 1.6;
            letter-spacing: 0.03em;
            background-color: var(--bg-primary);
        }
        
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Orbitron', sans-serif;
            font-weight: 700;
            margin-bottom: 1rem;
            letter-spacing: 0.05em;
            line-height: 1.2;
            text-transform: uppercase;
        }
        
        h1 {
            font-size: 2.5rem;
            color: var(--text-color);
            position: relative;
        }
        
        h2 {
            font-size: 2rem;
            color: var(--text-color);
            position: relative;
        }
        
        h3 {
            font-size: 1.5rem;
            color: var(--text-color);
        }
        
        p {
            margin-bottom: 1.25rem;
            line-height: 1.7;
        }
        
        /* Monospace for data displays */
        .neo-data {
            font-family: 'Share Tech Mono', monospace;
            letter-spacing: 0.05em;
        }
        
        /* Layout & Structure */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {display: none !important;}
        
        /* Force the entire app to take full height */
        .stApp {
            margin-top: -4rem !important;
            background-color: var(--bg-primary);
        }
        
        /* App container settings */
        .appview-container {
            padding-top: 0 !important;
        }
        
        /* Sidebar adjustments - futuristic panel */
        section[data-testid="stSidebar"] {
            top: 0 !important;
            padding-top: 1rem !important;
            background: var(--bg-secondary);
            border-right: 1px solid #e0e0e0;
            box-shadow: 5px 0 20px rgba(0, 0, 0, 0.5);
        }
        
        [data-testid="stSidebarContent"] {
            padding-top: 0 !important;
            margin-top: 0 !important;
        }
        
        /* Main content adjustments */
        .main .block-container {
            padding-top: 2rem !important;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        /* Ensure proper overflow handling */
        body {
            overflow-x: hidden;
        }
        
        /* Badges with hover effects */
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
            transition: all var(--transition-speed) ease;
        }
        
        .neo-badge {
            background-color: rgba(0, 0, 60, 0.1);
            color: var(--primary-color);
            border: 1px solid var(--primary-color);
            box-shadow: var(--neon-glow-cyan);
        }
        
        .neo-badge:hover {
            background-color: rgba(0, 0, 60, 0.15);
            box-shadow: var(--neon-glow-cyan-intense);
            transform: translateY(-2px);
        }
        
        .neo-upgrade-badge {
            background-color: rgba(255, 0, 228, 0.1);
            color: var(--primary-light);
            border: 1px solid var(--primary-light);
            box-shadow: var(--neon-glow-magenta);
        }
        
        .neo-upgrade-badge:hover {
            background-color: rgba(255, 0, 228, 0.15);
            box-shadow: var(--neon-glow-magenta-intense);
            transform: translateY(-2px);
        }
        
        /* Futuristic tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            border-bottom: none;
            padding-bottom: 0;
            background: transparent;
            display: flex;
            flex-wrap: wrap;
            justify-content: flex-start;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 16px 30px 16px 16px !important;
            margin: 5px 0 !important;
            border-radius: var(--border-radius) !important;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
            background-color: #FFFFFF !important;
            color: #000000 !important;
            border: 1px solid rgba(0, 0, 60, 0.2) !important;
            font-family: 'Share Tech Mono', monospace !important;
            font-weight: 700 !important;
            box-shadow: var(--box-shadow) !important;
            position: relative;
            overflow: hidden;
            text-transform: uppercase !important;
            letter-spacing: 0.1em !important;
            font-size: 0.9rem !important;
            min-width: 200px;
            text-align: center;
            width: auto !important;
            box-sizing: border-box !important;
        }
        
        .stTabs [data-baseweb="tab"]::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(229, 228, 226, 0.0);
            z-index: 0;
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        
        .stTabs [data-baseweb="tab"]:hover::before {
            opacity: 1;
        }
        
        /* Only apply hover effects to non-selected tabs */
        .stTabs [data-baseweb="tab"]:not([aria-selected="true"]):hover {
            background-color: #E5E4E2 !important;
            border: 1px solid var(--primary-color) !important;
            transform: translateY(-2px) !important;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #87CEEB !important;
            color: var(--primary-color) !important;
            font-weight: 700 !important;
            box-shadow: var(--neon-glow-cyan) !important;
            border: 1px solid var(--primary-color) !important;
        }
        
        /* Completely remove any red line or indicator from selected tabs */
        .stTabs [data-baseweb="tab"][aria-selected="true"]::after,
        .stTabs [data-baseweb="tab"][aria-selected="true"]::before,
        .stTabs [data-baseweb="tab-list"] [data-baseweb="tab"][aria-selected="true"]::after,
        .stTabs [data-baseweb="tab-list"] [data-baseweb="tab"][aria-selected="true"]::before {
            display: none !important;
            content: none !important;
            border: none !important;
            background: none !important;
            opacity: 0 !important;
            visibility: hidden !important;
        }
        
        /* Remove any hover effects that might show red lines */
        .stTabs [data-baseweb="tab-list"] [data-baseweb="tab"][aria-selected="true"]:hover::after,
        .stTabs [data-baseweb="tab-list"] [data-baseweb="tab"][aria-selected="true"]:hover::before {
            display: none !important;
            content: none !important;
            border: none !important;
            background: none !important;
        }
        
        /* Remove any indicator or highlight elements */
        .stTabs [data-baseweb="tab-highlight"],
        .stTabs [data-baseweb="tab-border"],
        .stTabs [role="tablist"] [data-baseweb="tab-highlight"],
        .stTabs [role="tablist"] [data-baseweb="tab-border"] {
            display: none !important;
            opacity: 0 !important;
            visibility: hidden !important;
            height: 0 !important;
            width: 0 !important;
            border: none !important;
            background: none !important;
        }
        
        .stTabs [aria-selected="true"]::after {
            content: "▶";
            position: absolute;
            top: 50%;
            right: 12px;
            transform: translateY(-50%);
            color: var(--primary-color);
            font-size: 0.75rem;
            text-shadow: var(--neon-glow-cyan);
        }
        
        /* Fix spacing around tab panels */
        .stTabs [data-baseweb="tab-panel"] {
            padding-top: 1.5rem !important;
            background: #f5f5f5;
            border-radius: var(--border-radius-lg);
            border: 1px solid #e0e0e0;
            padding: 1.5rem !important;
            margin-top: 0.8rem;
            box-shadow: var(--box-shadow);
        }
        
        /* Card styling with hover effects */
        .neo-card {
            background-color: white;
            border-radius: var(--border-radius);
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            border: 1px solid rgba(0, 0, 60, 0.1);
            box-shadow: var(--box-shadow);
            transition: all var(--transition-speed) ease;
        }
        
        .neo-card:hover {
            border: 1px solid rgba(0, 0, 60, 0.2);
            box-shadow: var(--box-shadow-hover);
            transform: translateY(-3px);
        }
        
        .neo-card-header {
            font-family: 'Share Tech Mono', sans-serif;
            font-size: 1.25rem;
            font-weight: 700;
            margin-bottom: 1rem;
            color: var(--primary-color);
            letter-spacing: 0.05em;
            text-transform: uppercase;
            transition: color var(--transition-speed) ease;
        }
        
        .neo-card:hover .neo-card-header {
            color: var(--accent-color);
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
        
        /* Table styling with hover effects */
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
            transition: background-color var(--transition-speed) ease;
        }
        
        .dataframe tr:hover th {
            background-color: rgba(0, 0, 60, 0.15);
        }
        
        .dataframe td {
            padding: 0.75rem;
            border: 1px solid rgba(0, 0, 60, 0.1);
            font-family: 'Share Tech Mono', monospace;
            transition: background-color var(--transition-speed) ease;
        }
        
        .dataframe tr:hover td {
            background-color: rgba(135, 206, 235, 0.1);
        }
        
        /* Navigation buttons with hover effects */
        .nav-button {
            margin-bottom: 10px;
            transition: all var(--transition-speed) ease;
        }
        
        .nav-button:hover {
            transform: translateY(-2px);
        }
        
        /* Button styling enhancements */
        button[data-testid="baseButton-primary"],
        button[data-testid="baseButton-secondary"] {
            transition: all var(--transition-speed) ease !important;
        }
        
        button[data-testid="baseButton-primary"]:hover,
        button[data-testid="baseButton-secondary"]:hover {
            transform: translateY(-2px) !important;
            box-shadow: var(--box-shadow-hover) !important;
        }
        
        /* Form elements hover effects */
        input[type="text"],
        input[type="number"],
        textarea,
        select {
            transition: all var(--transition-speed) ease !important;
            background-color: white !important;
        }
        
        /* Target the actual input elements to make them white */
        [data-baseweb="input"] input,
        [data-baseweb="textarea"] textarea,
        [data-baseweb="select"] input,
        [data-baseweb="select"] .react-select__control,
        [data-baseweb="select"] .react-select__menu {
            background-color: white !important;
        }
        
        /* Make sure the input containers have the tab panel color */
        [data-testid="stTextInput"] > div,
        [data-testid="stNumberInput"] > div,
        [data-testid="stTextArea"] > div,
        [data-baseweb="select"] > div,
        [data-testid="stMultiSelect"] > div {
            background-color: #f5f5f5 !important;
        }
        
        /* Ensure the actual input fields are white */
        .stTextInput input,
        .stNumberInput input,
        .stTextArea textarea,
        .stSelectbox select {
            background-color: white !important;
        }
        
        input[type="text"]:hover,
        input[type="number"]:hover,
        textarea:hover,
        select:hover {
            border-color: rgba(0, 0, 60, 0.3) !important;
            box-shadow: 0 0 5px rgba(0, 0, 60, 0.1) !important;
            background-color: white !important;
        }
        
        input[type="text"]:focus,
        input[type="number"]:focus,
        textarea:focus,
        select:focus {
            border-color: var(--accent-color) !important;
            box-shadow: var(--neon-glow-cyan) !important;
            transform: translateY(-1px) !important;
            background-color: white !important;
        }
        
        /* Additional rules to ensure white input fields */
        .stTextInput input,
        .stNumberInput input,
        .stTextArea textarea,
        .stSelectbox select,
        [data-baseweb="input"] input,
        [data-baseweb="textarea"] textarea,
        [data-baseweb="select"] input {
            background-color: white !important;
            color: var(--text-color) !important;
        }
        
        /* Make dropdown menus and options white */
        .stMultiSelect [data-baseweb="select"] div,
        .stMultiSelect [data-baseweb="popover"] div,
        .stMultiSelect [data-baseweb="menu"] div,
        .stMultiSelect [data-baseweb="select-option"] div,
        .stMultiSelect [role="listbox"],
        .stMultiSelect [role="option"],
        .stSelectbox [data-baseweb="select"] div,
        .stSelectbox [data-baseweb="popover"] div,
        .stSelectbox [data-baseweb="menu"] div,
        .stSelectbox [data-baseweb="select-option"] div,
        .stSelectbox [role="listbox"],
        .stSelectbox [role="option"] {
            background-color: white !important;
        }
        
        /* Target multiselect specifically */
        div[data-baseweb="select"] ul,
        div[data-baseweb="select"] ul li,
        div[data-baseweb="select"] div[role="listbox"],
        div[data-baseweb="select"] div[role="option"],
        div[data-baseweb="select"] div[data-testid="stMultiSelect"],
        .stMultiSelect div[role="combobox"] {
            background-color: white !important;
        }
        
        /* Slider hover effects */
        .stSlider:hover [data-baseweb="slider"] {
            box-shadow: var(--neon-glow-cyan) !important;
        }
        
        /* Radio button hover effects */
        .stRadio:hover [data-testid="stRadio"] {
            transform: translateY(-1px) !important;
        }
        
        /* Checkbox hover effects */
        .stCheckbox:hover [data-testid="stCheckbox"] {
            transform: scale(1.05) !important;
        }
        
        /* MultiSelect hover effects */
        .stMultiSelect:hover [data-baseweb="select"] {
            border-color: var(--accent-color) !important;
            box-shadow: var(--neon-glow-cyan) !important;
        }
        
        /* Chat styling with hover effects */
        .stChatMessage {
            padding: 1rem !important;
            margin-bottom: 1rem !important;
            border-radius: var(--border-radius) !important;
            transition: all var(--transition-speed) ease !important;
        }
        
        .stChatMessage:hover {
            box-shadow: var(--box-shadow-hover) !important;
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
            transition: all var(--transition-speed) ease !important;
        }
        
        .stChatInput:focus {
            border-color: var(--accent-color) !important;
            box-shadow: var(--neon-glow-cyan) !important;
        }
        
        /* Make chat container taller */
        [data-testid="stChatMessageContainer"] {
            min-height: 700px !important;
        }
        
        /* Apply styling to Streamlit's chat container */
        [data-testid="stChatContainer"] {
            background: linear-gradient(180deg, rgba(255,255,255,0.9), rgba(240,240,240,0.8)) !important;
            border-radius: 24px !important;
            box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.1) !important;
            border: 1px solid rgba(255, 255, 255, 0.7) !important;
            backdrop-filter: blur(10px) !important;
            padding: 1.5rem !important;
            position: relative !important;
            overflow: hidden !important;
            min-height: 800px !important;
        }
        
        /* Chat animations */
        @keyframes slideInRight {
            from {
                transform: translateX(30px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        @keyframes slideInLeft {
            from {
                transform: translateX(-30px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        /* Chat header styling */
        .neo-chat-header {
            display: flex;
            align-items: center;
            padding: 1rem;
            background: linear-gradient(135deg, #429de3, #87CEEB);
            border-radius: 16px;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 15px -5px rgba(0, 0, 0, 0.2);
        }
        
        .neo-chat-header h3 {
            color: white;
            margin: 0;
            font-family: 'Orbitron', sans-serif;
            letter-spacing: 0.1em;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }
        
        /* Sidebar navigation styling */
        .sidebar-nav-header {
            font-family: 'Share Tech Mono', sans-serif;
            font-size: 1rem;
            font-weight: 700;
            margin: 1rem 0 0.5rem 0;
            color: var(--primary-color);
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }
        
        .sidebar-icon {
            font-size: 1.5rem;
            text-align: center;
            transition: all var(--transition-speed) ease;
        }
        
        /* Sidebar button container */
        div[data-testid="column"] button {
            transition: all var(--transition-speed) ease !important;
        }
        
        div[data-testid="column"]:hover .sidebar-icon {
            transform: scale(1.2);
        }
        
        /* Expander hover effects */
        .streamlit-expanderHeader {
            transition: all var(--transition-speed) ease !important;
        }
        
        .streamlit-expanderHeader:hover {
            color: var(--accent-color) !important;
            background-color: rgba(0, 0, 60, 0.05) !important;
        }
        
        /* Footer styling */
        .neo-footer {
            text-align: center;
            color: #888;
            padding: 10px;
            font-family: 'Share Tech Mono', monospace;
            font-size: 0.9rem;
            border-radius: var(--border-radius);
            transition: all var(--transition-speed) ease;
        }
        
        .neo-footer:hover {
            color: var(--primary-color);
            background-color: rgba(0, 0, 60, 0.03);
            box-shadow: var(--neon-glow-cyan);
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
        # Add app title with gradient background at the top of the sidebar
        st.markdown("""
        <div style="background: linear-gradient(90deg, #429de3, #87CEEB);
                    padding: 15px;
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);">
            <h1 style="color: #000000;
                    font-family: 'Trebuchet MS', sans-serif;
                    text-align: center;
                    letter-spacing: 2px;
                    font-weight: 600;
                    text-transform: uppercase;
                    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);">
                    VIRTUAL DOCTOR
            </h1>
        </div>
        """, unsafe_allow_html=True)
        
        # Initialize current_view in session state if it doesn't exist
        if 'current_view' not in st.session_state:
            st.session_state.current_view = "input_data"  # Default view
        
        # Navigation section
        st.markdown("<div class='sidebar-nav-header'>Navigation</div>", unsafe_allow_html=True)
        
        # Input Data button
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown("<div class='sidebar-icon'>📋</div>", unsafe_allow_html=True)
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
            st.markdown("<div class='sidebar-icon'>🩺</div>", unsafe_allow_html=True)
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
    
    # All tabs are now optional
    return True

# Function to get completion status for all tabs
def get_tab_completion_status():
    tabs = ["Basic Info", "Physical Metrics", "Symptoms", "Medical History", "Medications", "Family History"]
    return {tab: is_tab_complete(tab) for tab in tabs}

# Function to validate if all required fields are filled
def validate_form_completion():
    # All fields are now optional, so form is always complete
    return True

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
        gender = col2.selectbox(
            "Gender",
            options=["Male", "Female", "Other"],
            index=["Male", "Female", "Other"].index(st.session_state.patient_info["basic"]["gender"]) if st.session_state.patient_info["basic"]["gender"] in ["Male", "Female", "Other"] else 0
        )
    
    # All fields are optional now
    tab.info("All fields in this tab are optional.")
    
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
        severity = col2.number_input(
            "On a scale of 1-10, how severe is your main concern?",
            min_value=1,
            max_value=10,
            value=int(st.session_state.patient_info["symptoms"]["severity"]) if st.session_state.patient_info["symptoms"]["severity"] else 1,
            help="1 = Very mild, 10 = Extremely severe",
            step=1
        )
    
    # Additional symptoms multi-select
    tab.markdown("**Additional Symptoms**")
    additional = tab.multiselect(
        "Are you experiencing any other symptoms?",
        options=COMMON_SYMPTOMS,
        default=st.session_state.patient_info["symptoms"]["additional"],
        help="Select all that apply"
    )
    
    # All fields are optional now
    tab.info("All fields in this tab are optional.")
    
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
    
    # Create HTML for a simple two-column table with hover effects
    html = "<table style='width:100%; border-collapse: collapse;'>"
    html += "<tr><th style='background-color: rgba(0, 0, 60, 0.1); color: #00003c; padding: 0.75rem; border: 1px solid rgba(0, 0, 60, 0.2); transition: all 0.3s ease;'>Field</th>"
    html += "<th style='background-color: rgba(0, 0, 60, 0.1); color: #00003c; padding: 0.75rem; border: 1px solid rgba(0, 0, 60, 0.2); transition: all 0.3s ease;'>Value</th></tr>"
    
    for i in range(len(df)):
        html += f"<tr style='transition: all 0.3s ease;' onmouseover=\"this.style.backgroundColor='rgba(135, 206, 235, 0.1)';\" onmouseout=\"this.style.backgroundColor='transparent';\">"
        html += f"<td style='padding: 0.75rem; border: 1px solid rgba(0, 0, 60, 0.1); transition: all 0.3s ease;'>{df['Field'][i]}</td>"
        html += f"<td style='padding: 0.75rem; border: 1px solid rgba(0, 0, 60, 0.1); transition: all 0.3s ease;'>{df['Value'][i]}</td></tr>"
    
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
    
    # All fields are now optional
    form_complete = validate_form_completion()
    # Since all fields are optional, this will always be true
    tab.success("You can now submit the form.")
    
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
    
    # Display conversation history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # User input area - make it larger
    user_input = st.chat_input("Type your message here...", key="chat_input")
    
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
    st.markdown("""
    <div class="neo-footer">
        <p>Virtual Doctor Assistant | Developed by: Senthil Palanivelu</p>
        <p style="font-size: 12px; margin-top: 5px;">Version 1.0.0</p>
    </div>
    """, unsafe_allow_html=True)

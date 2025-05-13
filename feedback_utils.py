import pandas as pd
import os
import datetime
import uuid
import streamlit as st
from collections import Counter
import re

# Function to generate a unique session ID
def generate_session_id():
    """Generate a unique session ID for tracking feedback"""
    return str(uuid.uuid4())

# Function to save feedback to CSV file
def save_feedback(feedback_data):
    """
    Save feedback data to a CSV file
    
    Args:
        feedback_data (dict): Dictionary containing feedback information
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create feedback directory if it doesn't exist
        os.makedirs('feedback', exist_ok=True)
        
        # Path to feedback CSV file
        feedback_file = 'feedback/user_feedback.csv'
        
        # Add timestamp if not already present
        if not feedback_data.get('timestamp'):
            feedback_data['timestamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Create DataFrame from feedback data
        df = pd.DataFrame([feedback_data])
        
        # Check if file exists
        if os.path.exists(feedback_file):
            # Append to existing file
            df.to_csv(feedback_file, mode='a', header=False, index=False)
        else:
            # Create new file with header
            df.to_csv(feedback_file, index=False)
            
        return True
    
    except Exception as e:
        st.error(f"Error saving feedback: {e}")
        return False

# Function to load feedback data
def load_feedback_data():
    """
    Load feedback data from CSV file
    
    Returns:
        pandas.DataFrame: DataFrame containing feedback data or None if file doesn't exist
    """
    try:
        feedback_file = 'feedback/user_feedback.csv'
        
        if os.path.exists(feedback_file):
            return pd.read_csv(feedback_file)
        else:
            return None
    
    except Exception as e:
        st.error(f"Error loading feedback data: {e}")
        return None

# Function to calculate average ratings
def calculate_average_ratings(feedback_df):
    """
    Calculate average ratings from feedback data
    
    Args:
        feedback_df (pandas.DataFrame): DataFrame containing feedback data
    
    Returns:
        dict: Dictionary containing average ratings for each category
    """
    if feedback_df is None or len(feedback_df) == 0:
        return {
            'overall': 0,
            'helpfulness': 0,
            'clarity': 0,
            'empathy': 0,
            'accuracy': 0
        }
    
    return {
        'overall': feedback_df['overall_rating'].mean(),
        'helpfulness': feedback_df['helpfulness_rating'].mean(),
        'clarity': feedback_df['clarity_rating'].mean(),
        'empathy': feedback_df['empathy_rating'].mean(),
        'accuracy': feedback_df['accuracy_rating'].mean()
    }

# Function to extract common themes from comments
def extract_common_themes(feedback_df, min_count=2):
    """
    Extract common words/themes from feedback comments
    
    Args:
        feedback_df (pandas.DataFrame): DataFrame containing feedback data
        min_count (int): Minimum count to include a word in results
    
    Returns:
        dict: Dictionary of common words and their counts
    """
    if feedback_df is None or len(feedback_df) == 0 or 'comments' not in feedback_df.columns:
        return {}
    
    # Combine all comments
    all_comments = ' '.join(feedback_df['comments'].fillna('').astype(str))
    
    # Convert to lowercase and remove punctuation
    all_comments = all_comments.lower()
    all_comments = re.sub(r'[^\w\s]', ' ', all_comments)
    
    # Split into words
    words = all_comments.split()
    
    # Remove common stop words
    stop_words = {'the', 'and', 'is', 'in', 'it', 'to', 'i', 'a', 'was', 'that', 'this', 
                 'of', 'for', 'my', 'with', 'me', 'you', 'very', 'are', 'on', 'your',
                 'be', 'have', 'not', 'but', 'had', 'has', 'would', 'could', 'should'}
    
    filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
    
    # Count word frequencies
    word_counts = Counter(filtered_words)
    
    # Filter by minimum count
    common_themes = {word: count for word, count in word_counts.items() if count >= min_count}
    
    # Sort by frequency (descending)
    return dict(sorted(common_themes.items(), key=lambda x: x[1], reverse=True))

# Function to get feedback statistics
def get_feedback_statistics():
    """
    Get statistics from feedback data
    
    Returns:
        tuple: (total_count, average_ratings, common_themes)
    """
    feedback_df = load_feedback_data()
    
    if feedback_df is None:
        return 0, calculate_average_ratings(None), {}
    
    total_count = len(feedback_df)
    average_ratings = calculate_average_ratings(feedback_df)
    common_themes = extract_common_themes(feedback_df)
    
    return total_count, average_ratings, common_themes

# Function to initialize feedback session
def initialize_feedback_session():
    """Initialize a new feedback session with a unique ID"""
    if 'feedback_session_id' not in st.session_state:
        st.session_state.feedback_session_id = generate_session_id()
    
    if 'feedback_submitted' not in st.session_state:
        st.session_state.feedback_submitted = False
    
    if 'feedback_data' not in st.session_state:
        st.session_state.feedback_data = {
            "overall_rating": 0,
            "helpfulness_rating": 0,
            "clarity_rating": 0,
            "empathy_rating": 0,
            "accuracy_rating": 0,
            "comments": "",
            "session_id": st.session_state.feedback_session_id,
            "timestamp": "",
            "conversation_length": 0,
            "model_used": ""
        }

# Function to reset feedback session
def reset_feedback_session():
    """Reset the feedback session state"""
    st.session_state.feedback_session_id = generate_session_id()
    st.session_state.feedback_submitted = False
    st.session_state.feedback_data = {
        "overall_rating": 0,
        "helpfulness_rating": 0,
        "clarity_rating": 0,
        "empathy_rating": 0,
        "accuracy_rating": 0,
        "comments": "",
        "session_id": st.session_state.feedback_session_id,
        "timestamp": "",
        "conversation_length": 0,
        "model_used": ""
    }

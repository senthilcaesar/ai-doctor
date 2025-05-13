import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from feedback_utils import load_feedback_data, get_feedback_statistics

# Set page config
st.set_page_config(
    page_title="Virtual Doctor Feedback Dashboard",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
    .dashboard-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: #00003c;
        text-align: center;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    
    .dashboard-subtitle {
        font-family: 'Share Tech Mono', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: #00003c;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    
    
    .stat-value {
        font-family: 'Share Tech Mono', monospace;
        font-size: 3rem;
        font-weight: 700;
        color: #00003c;
        text-align: center;
    }
    
    .stat-label {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.2rem;
        color: #666666;
        text-align: center;
        margin-top: 0.5rem;
    }
    
    .chart-container {
        background-color: white;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(0, 0, 60, 0.1);
        box-shadow: 0 2px 10px -2px rgba(0, 0, 0, 0.05);
    }
    
    .theme-item {
        background-color: rgba(0, 0, 60, 0.05);
        border-radius: 8px;
        padding: 0.5rem 1rem;
        margin-bottom: 0.5rem;
        font-family: 'Rajdhani', sans-serif;
        transition: all 0.3s ease;
    }
    
    .theme-item:hover {
        background-color: rgba(0, 0, 60, 0.1);
        transform: translateX(5px);
    }
    
    .theme-count {
        font-family: 'Share Tech Mono', monospace;
        font-weight: 700;
        color: #00003c;
        float: right;
    }
    
    .no-data {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.2rem;
        color: #666666;
        text-align: center;
        padding: 2rem;
        background-color: rgba(0, 0, 60, 0.05);
        border-radius: 16px;
    }
</style>
""", unsafe_allow_html=True)

# Main dashboard title
st.markdown("<div class='dashboard-title'>Virtual Doctor Feedback Dashboard</div>", unsafe_allow_html=True)

# Load feedback data
feedback_df = load_feedback_data()

if feedback_df is None or len(feedback_df) == 0:
    st.markdown("<div class='no-data'>No feedback data available yet. Feedback will appear here once users start providing it.</div>", unsafe_allow_html=True)
else:
    # Get feedback statistics
    total_count, average_ratings, common_themes = get_feedback_statistics()
    
    # Display key statistics
    st.markdown("<div class='dashboard-subtitle'>Key Statistics</div>", unsafe_allow_html=True)
    
    # Create three columns for key stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"<div class='stat-value'>{total_count}</div>", unsafe_allow_html=True)
        st.markdown("<div class='stat-label'>Total Feedback Submissions</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"<div class='stat-value'>{average_ratings['overall']:.1f}</div>", unsafe_allow_html=True)
        st.markdown("<div class='stat-label'>Average Overall Rating</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        # Calculate percentage of positive ratings (4 or 5 stars)
        positive_ratings = len(feedback_df[feedback_df['overall_rating'] >= 4])
        positive_percentage = (positive_ratings / total_count) * 100 if total_count > 0 else 0
        
        st.markdown(f"<div class='stat-value'>{positive_percentage:.1f}%</div>", unsafe_allow_html=True)
        st.markdown("<div class='stat-label'>Positive Feedback Rate</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Display detailed ratings
    st.markdown("<div class='dashboard-subtitle'>Rating Breakdown</div>", unsafe_allow_html=True)
    
    # Create two columns for charts
    col1, col2 = st.columns(2)
    
    with col1:
        
        # Create a bar chart for average ratings by category
        fig, ax = plt.subplots(figsize=(10, 6))
        
        categories = ['Overall', 'Helpfulness', 'Clarity', 'Empathy', 'Accuracy']
        values = [
            average_ratings['overall'],
            average_ratings['helpfulness'],
            average_ratings['clarity'],
            average_ratings['empathy'],
            average_ratings['accuracy']
        ]
        
        # Create horizontal bar chart
        bars = ax.barh(categories, values, color='#429de3')
        
        # Add value labels to the bars
        for i, v in enumerate(values):
            ax.text(v + 0.1, i, f"{v:.1f}", va='center')
        
        # Set chart properties
        ax.set_xlim(0, 5.5)  # Rating scale is 1-5
        ax.set_xlabel('Average Rating')
        ax.set_title('Average Ratings by Category')
        ax.grid(axis='x', linestyle='--', alpha=0.7)
        
        # Display the chart
        st.pyplot(fig)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        
        # Create a histogram for overall rating distribution
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Create histogram
        sns.histplot(data=feedback_df, x='overall_rating', bins=5, kde=False, ax=ax, color='#429de3')
        
        # Set chart properties
        ax.set_xlim(0.5, 5.5)  # Rating scale is 1-5
        ax.set_xticks([1, 2, 3, 4, 5])
        ax.set_xlabel('Rating')
        ax.set_ylabel('Count')
        ax.set_title('Distribution of Overall Ratings')
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Display the chart
        st.pyplot(fig)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Display common themes from comments
    st.markdown("<div class='dashboard-subtitle'>Common Themes in Feedback</div>", unsafe_allow_html=True)
    
    if common_themes:
        # Create two columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            
            # Create a bar chart for common themes
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Get top 10 themes
            top_themes = dict(list(common_themes.items())[:10])
            
            # Create horizontal bar chart
            bars = ax.barh(list(top_themes.keys()), list(top_themes.values()), color='#429de3')
            
            # Add value labels to the bars
            for i, v in enumerate(top_themes.values()):
                ax.text(v + 0.1, i, str(v), va='center')
            
            # Set chart properties
            ax.set_xlabel('Frequency')
            ax.set_title('Top 10 Common Themes in Feedback')
            ax.grid(axis='x', linestyle='--', alpha=0.7)
            
            # Display the chart
            st.pyplot(fig)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            
            # Display themes as a list
            for theme, count in common_themes.items():
                st.markdown(f"<div class='theme-item'>{theme} <span class='theme-count'>{count}</span></div>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='no-data'>No common themes found in feedback comments.</div>", unsafe_allow_html=True)
    
    # Display recent feedback
    st.markdown("<div class='dashboard-subtitle'>Recent Feedback</div>", unsafe_allow_html=True)
    
    # Sort by timestamp (most recent first)
    recent_feedback = feedback_df.sort_values(by='timestamp', ascending=False).head(5)
    
    if not recent_feedback.empty:
        for _, row in recent_feedback.iterrows():
            with st.expander(f"Feedback from {row['timestamp']} (Overall: {row['overall_rating']}/5)"):
                st.write(f"**Helpfulness:** {row['helpfulness_rating']}/5")
                st.write(f"**Clarity:** {row['clarity_rating']}/5")
                st.write(f"**Empathy:** {row['empathy_rating']}/5")
                st.write(f"**Accuracy:** {row['accuracy_rating']}/5")
                
                if row['comments']:
                    st.write("**Comments:**")
                    st.write(row['comments'])
                else:
                    st.write("**Comments:** No comments provided")
    else:
        st.markdown("<div class='no-data'>No recent feedback available.</div>", unsafe_allow_html=True)
    
    # Add download button for the feedback data
    st.markdown("<div class='dashboard-subtitle'>Export Data</div>", unsafe_allow_html=True)
    
    csv = feedback_df.to_csv(index=False)
    st.download_button(
        label="Download Feedback Data as CSV",
        data=csv,
        file_name="virtual_doctor_feedback.csv",
        mime="text/csv",
    )

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; padding: 10px; font-family: 'Share Tech Mono', monospace; font-size: 0.9rem;">
    <p>Virtual Doctor Assistant Feedback Dashboard | Developed by: Senthil Palanivelu</p>
    <p style="font-size: 12px; margin-top: 5px;">Version 1.0.0</p>
</div>
""", unsafe_allow_html=True)

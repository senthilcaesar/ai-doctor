import streamlit as st
import re
from serp_service import SerpService

def initialize_serp_service():
    """
    Initialize the SERP service with API key from Streamlit secrets.
    
    Returns:
        SerpService or None: Initialized SERP service or None if initialization fails
    """
    try:
        api_key = st.secrets.get("SERP_API_KEY")
        if not api_key:
            st.warning("SERP API key not found in secrets. Web search features will be disabled.")
            return None
        
        return SerpService(api_key=api_key)
    except Exception as e:
        st.error(f"Error initializing SERP service: {e}")
        return None

def should_enhance_with_serp(user_input, agent_response):
    """
    Determine if the agent's response should be enhanced with SERP data.
    
    Args:
        user_input (str): The user's input message
        agent_response (str): The agent's initial response
        
    Returns:
        bool: True if the response should be enhanced, False otherwise
    """
    # Check if the response indicates uncertainty or need for more information
    uncertainty_phrases = [
        "I don't have specific information",
        "I don't have the latest",
        "I'm not aware of the latest",
        "I don't have access to",
        "I don't have enough information",
        "I'm not familiar with",
        "I would need to research",
        "I can't provide details on",
        "I don't have current data",
        "I don't have up-to-date",
        "I'm not able to access",
        "I don't have the most recent",
        "without access to",
        "would require access to",
        "I cannot access",
        "I'm limited in my ability to",
        "I don't have information about specific",
        "I cannot provide specific"
    ]
    
    needs_enhancement = any(phrase.lower() in agent_response.lower() for phrase in uncertainty_phrases)
    
    # Also check if user is explicitly asking about recent developments
    recency_phrases = [
        "latest research",
        "recent studies",
        "new treatment",
        "latest guidelines",
        "recent development",
        "new findings",
        "latest news",
        "current research",
        "recent advances",
        "new discoveries",
        "latest medical",
        "recent medical",
        "new medical",
        "latest health",
        "recent health",
        "new health",
        "latest clinical",
        "recent clinical",
        "new clinical",
        "latest therapy",
        "recent therapy",
        "new therapy",
        "latest drug",
        "recent drug",
        "new drug"
    ]
    
    needs_enhancement = needs_enhancement or any(phrase.lower() in user_input.lower() for phrase in recency_phrases)
    
    # Check if the user is asking about a specific medical condition or treatment
    medical_query_indicators = [
        "what is",
        "what are",
        "how to treat",
        "how to manage",
        "symptoms of",
        "causes of",
        "treatment for",
        "cure for",
        "therapy for",
        "medication for",
        "drug for",
        "how do you treat",
        "how do you manage",
        "how do you cure",
        "how do you diagnose",
        "how is it diagnosed",
        "how is it treated",
        "how is it managed",
        "how is it cured",
        "what are the symptoms of",
        "what are the causes of",
        "what are the treatments for",
        "what are the medications for",
        "what are the therapies for",
        "what are the drugs for"
    ]
    
    # Check if the user's input contains any of the medical query indicators
    contains_medical_query = any(indicator.lower() in user_input.lower() for indicator in medical_query_indicators)
    
    # Check if the agent's response is relatively short, which might indicate limited information
    is_short_response = len(agent_response.split()) < 100
    
    # Enhance if it's a medical query with a short response
    needs_enhancement = needs_enhancement or (contains_medical_query and is_short_response)
    
    return needs_enhancement

def extract_medical_entities(text):
    """
    Extract potential medical entities from text.
    This is a simplified approach - in production, use a medical NER model.
    
    Args:
        text (str): The text to extract entities from
        
    Returns:
        list: List of potential medical entities
    """
    # Common medical condition suffixes
    medical_suffixes = [
        "itis", "emia", "oma", "pathy", "osis", "iasis", "ism", 
        "disease", "disorder", "syndrome", "infection", "condition"
    ]
    
    # Extract words that might be medical conditions
    words = re.findall(r'\b[a-zA-Z]+(?:-[a-zA-Z]+)*\b', text)
    
    # Filter for potential medical terms
    medical_entities = []
    for word in words:
        # Check if the word ends with a medical suffix
        if any(word.lower().endswith(suffix) for suffix in medical_suffixes):
            medical_entities.append(word)
        # Check if the word is capitalized (might be a proper medical term)
        elif word[0].isupper() and len(word) > 3 and word.lower() not in ["what", "how", "when", "where", "why", "who", "which"]:
            medical_entities.append(word)
    
    # Add multi-word medical terms
    multi_word_patterns = [
        r'\b[A-Z][a-z]+ (disease|disorder|syndrome|infection|condition)\b',
        r'\b[a-z]+ (disease|disorder|syndrome|infection|condition)\b',
        r'\b(Type [0-9]+|type [0-9]+) [a-zA-Z]+\b'
    ]
    
    for pattern in multi_word_patterns:
        matches = re.findall(pattern, text)
        if matches:
            multi_word_terms = re.findall(pattern, text)
            medical_entities.extend(multi_word_terms)
    
    return list(set(medical_entities))

def enhance_with_serp(user_input, agent_response):
    """
    Enhance the agent's response with SERP data when appropriate.
    
    Args:
        user_input (str): The user's input message
        agent_response (str): The agent's initial response
        
    Returns:
        str: Enhanced response with SERP data if applicable, otherwise the original response
    """
    if not should_enhance_with_serp(user_input, agent_response) or 'serp_service' not in st.session_state:
        return agent_response
    
    try:
        # Extract potential medical entities from the user input
        medical_entities = extract_medical_entities(user_input)
        
        # If no medical entities found, use the whole user input as the search query
        if not medical_entities:
            search_query = user_input
        else:
            # Use the first medical entity as the search query
            search_query = medical_entities[0]
        
        # Get search results
        search_results = st.session_state.serp_service.search_medical_info(search_query)
        
        if search_results:
            # Generate appropriate disclaimer
            disclaimer = st.session_state.serp_service.generate_medical_disclaimer(search_results)
            
            # Format the search results as a supplement to the agent's response
            serp_supplement = "\n\n**Additional Information from Medical Sources:**\n\n"
            
            # Prioritize trusted sources
            trusted_results = [result for result in search_results if result.get("is_trusted", False)]
            untrusted_results = [result for result in search_results if not result.get("is_trusted", False)]
            
            # Use trusted results first, then untrusted if needed
            results_to_show = trusted_results + untrusted_results
            
            for i, result in enumerate(results_to_show[:3], 1):
                source_indicator = "✓ " if result.get("is_trusted", False) else ""
                serp_supplement += f"{i}. **{source_indicator}{result['title']}**\n"
                serp_supplement += f"   {result['snippet']}\n"
                serp_supplement += f"   Source: [{result['link']}]({result['link']})\n\n"
            
            serp_supplement += f"\n*{disclaimer}*"
            
            # Combine the original response with the SERP supplement
            enhanced_response = agent_response + serp_supplement
            return enhanced_response
        
    except Exception as e:
        # Log the error but return the original response
        print(f"Error enhancing response with SERP data: {e}")
    
    # Return the original response if no enhancement was needed or possible
    return agent_response

def get_latest_medical_news(topic=None):
    """
    Get the latest medical news on a specific topic or general medical news.
    
    Args:
        topic (str, optional): The medical topic to get news for. Defaults to None.
        
    Returns:
        str: Formatted medical news or empty string if no news found
    """
    if 'serp_service' not in st.session_state:
        return ""
    
    try:
        # If no topic provided, use general medical news
        search_topic = topic or "medical health research"
        
        # Get news results
        news_results = st.session_state.serp_service.get_medical_news(search_topic)
        
        if news_results:
            # Format the news results
            news_formatted = "\n\n**Latest Medical News:**\n\n"
            
            # Prioritize trusted sources
            trusted_news = [result for result in news_results if result.get("is_trusted", False)]
            untrusted_news = [result for result in news_results if not result.get("is_trusted", False)]
            
            # Use trusted news first, then untrusted if needed
            news_to_show = trusted_news + untrusted_news
            
            for i, result in enumerate(news_to_show[:3], 1):
                source_indicator = "✓ " if result.get("is_trusted", False) else ""
                news_formatted += f"{i}. **{source_indicator}{result['title']}**\n"
                if result.get("date"):
                    news_formatted += f"   Date: {result['date']}\n"
                if result.get("source"):
                    news_formatted += f"   Source: {result['source']}\n"
                news_formatted += f"   [Read more]({result['link']})\n\n"
            
            news_formatted += "\n*Note: This news was retrieved from web sources and should be verified with healthcare professionals.*"
            
            return news_formatted
        
    except Exception as e:
        # Log the error but return empty string
        print(f"Error getting medical news: {e}")
    
    return ""

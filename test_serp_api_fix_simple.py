"""
Simple test script to verify the fix for the SerpAPI issue.
This script tests the updated implementation of the SerpService class.
"""

import os
import sys
import json
import toml
from serp_service import SerpService

def load_api_key():
    """Load SERP API key from .streamlit/secrets.toml file."""
    try:
        # Try to load from .streamlit/secrets.toml
        secrets_path = os.path.join('.streamlit', 'secrets.toml')
        if os.path.exists(secrets_path):
            secrets = toml.load(secrets_path)
            api_key = secrets.get('SERP_API_KEY')
            if api_key and api_key != 'your-serp-api-key-here':
                return api_key
        
        # If not found or invalid, check environment variable
        api_key = os.environ.get('SERP_API_KEY')
        if api_key:
            return api_key
        
        print("Error: SERP API key not found in .streamlit/secrets.toml or environment variables.")
        print("Please add your SERP API key to .streamlit/secrets.toml or set the SERP_API_KEY environment variable.")
        sys.exit(1)
    
    except Exception as e:
        print(f"Error loading API key: {e}")
        sys.exit(1)

def test_search_medical_info():
    """Test the search_medical_info method with the updated implementation."""
    api_key = load_api_key()
    serp_service = SerpService(api_key=api_key)
    
    print("\n=== Testing search_medical_info Method ===")
    
    # Test query
    query = "Diabetes"
    
    print(f"Searching for: {query}")
    
    try:
        # Search for medical information
        results = serp_service.search_medical_info(query)
        
        # Display results
        if results:
            print(f"Found {len(results)} results:")
            for i, result in enumerate(results, 1):
                trusted_indicator = "✓ " if result.get("is_trusted", False) else ""
                print(f"\n{i}. {trusted_indicator}{result['title']}")
                print(f"   {result['snippet']}")
                print(f"   Source: {result['link']}")
            
            # Generate disclaimer
            disclaimer = serp_service.generate_medical_disclaimer(results)
            print(f"\nDisclaimer: {disclaimer}")
        else:
            print("No results found.")
    
    except Exception as e:
        print(f"Error searching for '{query}': {e}")

def test_get_medical_news():
    """Test the get_medical_news method with the updated implementation."""
    api_key = load_api_key()
    serp_service = SerpService(api_key=api_key)
    
    print("\n=== Testing get_medical_news Method ===")
    
    # Test topic
    topic = "Diabetes"
    
    print(f"Getting news for: {topic}")
    
    try:
        # Get medical news
        news_results = serp_service.get_medical_news(topic)
        
        # Display results
        if news_results:
            print(f"Found {len(news_results)} news results:")
            for i, result in enumerate(news_results, 1):
                trusted_indicator = "✓ " if result.get("is_trusted", False) else ""
                print(f"\n{i}. {trusted_indicator}{result['title']}")
                if result.get('date'):
                    print(f"   Date: {result['date']}")
                if result.get('source'):
                    print(f"   Source: {result['source']}")
                print(f"   Link: {result['link']}")
        else:
            print("No news found.")
    
    except Exception as e:
        print(f"Error getting news for '{topic}': {e}")

def main():
    """Main function to run all tests."""
    print("\nTesting Fixed SerpAPI Implementation")
    print("==================================")
    
    # Test search_medical_info method
    test_search_medical_info()
    
    # Test get_medical_news method
    test_get_medical_news()
    
    print("\nAll tests completed.")

if __name__ == "__main__":
    main()

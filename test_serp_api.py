"""
Test script for SERP API integration with Virtual Doctor Assistant.
This script demonstrates how to use the SERP API service to retrieve medical information.

Usage:
    python test_serp_api.py

Requirements:
    - SERP API key in .streamlit/secrets.toml
    - serpapi-python package installed
"""

import os
import sys
import json
import toml
import serpapi
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

def test_medical_search():
    """Test searching for medical information."""
    api_key = load_api_key()
    serp_service = SerpService(api_key=api_key)
    
    # Test queries
    test_queries = [
        "diabetes treatment guidelines",
        "covid-19 symptoms",
        "hypertension management",
        "migraine prevention",
        "asthma inhaler types"
    ]
    
    for query in test_queries:
        print(f"\n{'='*80}")
        print(f"SEARCHING FOR: {query}")
        print(f"{'='*80}")
        
        try:
            # Search for medical information
            results = serp_service.search_medical_info(query, num_results=3)
            
            # Display results
            if results:
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

def test_medical_news():
    """Test retrieving medical news."""
    api_key = load_api_key()
    serp_service = SerpService(api_key=api_key)
    
    # Test topics
    test_topics = [
        "diabetes research",
        "covid-19 vaccine",
        "heart disease prevention"
    ]
    
    for topic in test_topics:
        print(f"\n{'='*80}")
        print(f"GETTING NEWS FOR: {topic}")
        print(f"{'='*80}")
        
        try:
            # Get medical news
            news_results = serp_service.get_medical_news(topic, num_results=3)
            
            # Display results
            if news_results:
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

def test_source_validation():
    """Test source validation."""
    api_key = load_api_key()
    serp_service = SerpService(api_key=api_key)
    
    # Test URLs
    test_urls = [
        "https://www.mayoclinic.org/diseases-conditions/diabetes/symptoms-causes/syc-20371444",
        "https://www.cdc.gov/coronavirus/2019-ncov/symptoms-testing/symptoms.html",
        "https://www.nih.gov/health-information",
        "https://www.who.int/health-topics/coronavirus",
        "https://example.com/health-article",
        "https://randomwebsite.com/medical-advice"
    ]
    
    print(f"\n{'='*80}")
    print(f"TESTING SOURCE VALIDATION")
    print(f"{'='*80}")
    
    for url in test_urls:
        is_trusted = serp_service.validate_medical_source(url)
        status = "✓ Trusted" if is_trusted else "✗ Not trusted"
        print(f"{status}: {url}")

def main():
    """Main function to run all tests."""
    print("\nTesting SERP API Integration for Virtual Doctor Assistant")
    print("--------------------------------------------------------\n")
    
    # Test medical search
    test_medical_search()
    
    # Test medical news
    test_medical_news()
    
    # Test source validation
    test_source_validation()
    
    print("\nAll tests completed.")

if __name__ == "__main__":
    main()

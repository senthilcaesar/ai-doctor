"""
Simple script to test the SERP API key directly using the requests library.
This will help determine if the issue is with the API key or with the serpapi package.
"""

import os
import sys
import json
import toml
import requests

def load_api_key():
    """Load SERP API key from .streamlit/secrets.toml file."""
    try:
        # Try to load from .streamlit/secrets.toml
        secrets_path = os.path.join('.streamlit', 'secrets.toml')
        if os.path.exists(secrets_path):
            secrets = toml.load(secrets_path)
            api_key = secrets.get('SERP_API_KEY')
            if api_key:
                return api_key
        
        # If not found, check environment variable
        api_key = os.environ.get('SERP_API_KEY')
        if api_key:
            return api_key
        
        print("Error: SERP API key not found in .streamlit/secrets.toml or environment variables.")
        print("Please add your SERP API key to .streamlit/secrets.toml or set the SERP_API_KEY environment variable.")
        sys.exit(1)
    
    except Exception as e:
        print(f"Error loading API key: {e}")
        sys.exit(1)

def test_serp_api_direct():
    """Test the SERP API key directly using the requests library."""
    api_key = load_api_key()
    
    print(f"Using API key: {api_key}")
    
    # Test query
    query = "diabetes treatment guidelines"
    
    # Build the URL
    url = "https://serpapi.com/search"
    
    # Build the parameters
    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key,
        "num": 3,
        "safe": "active"
    }
    
    print(f"Making request to: {url}")
    print(f"With parameters: {params}")
    
    try:
        # Make the request
        response = requests.get(url, params=params)
        
        # Check if the request was successful
        if response.status_code == 200:
            print("Request successful!")
            
            # Parse the response
            data = response.json()
            
            # Print the organic results
            if "organic_results" in data:
                print("\nOrganic Results:")
                for i, result in enumerate(data["organic_results"][:3], 1):
                    print(f"\n{i}. {result.get('title', '')}")
                    print(f"   {result.get('snippet', '')}")
                    print(f"   Source: {result.get('link', '')}")
            else:
                print("\nNo organic results found in the response.")
                print("Response data:")
                print(json.dumps(data, indent=2))
        else:
            print(f"Request failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
    
    except Exception as e:
        print(f"Error making request: {e}")

if __name__ == "__main__":
    test_serp_api_direct()

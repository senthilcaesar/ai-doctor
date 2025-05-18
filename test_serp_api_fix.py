"""
Test script to diagnose and fix the SerpAPI issue.
This script tests different approaches to the site search parameter.
"""

import os
import sys
import json
import toml
import serpapi

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

def test_original_query():
    """Test the original query that's failing."""
    api_key = load_api_key()
    
    print("\n=== Testing Original Query ===")
    
    # Original parameters that are failing
    params = {
        "engine": "google",
        "q": "Diabetes medical information health",
        "api_key": api_key,
        "num": "5",
        "as_sitesearch": "mayoclinic.org,medlineplus.gov,nih.gov,who.int,cdc.gov",
        "safe": "active"
    }
    
    print(f"Query: {params['q']}")
    print(f"Site search: {params['as_sitesearch']}")
    
    try:
        results = serpapi.search(params)
        print_results(results)
    except Exception as e:
        print(f"Error: {e}")

def test_site_operator():
    """Test using the site: operator in the query instead of as_sitesearch parameter."""
    api_key = load_api_key()
    
    print("\n=== Testing site: Operator ===")
    
    # Using site: operator in the query
    sites = ["mayoclinic.org", "medlineplus.gov", "nih.gov", "who.int", "cdc.gov"]
    site_query = " OR ".join([f"site:{site}" for site in sites])
    query = f"Diabetes medical information health ({site_query})"
    
    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key,
        "num": "5",
        "safe": "active"
    }
    
    print(f"Query: {params['q']}")
    
    try:
        results = serpapi.search(params)
        print_results(results)
    except Exception as e:
        print(f"Error: {e}")

def test_individual_sites():
    """Test each site individually to see which ones work."""
    api_key = load_api_key()
    
    print("\n=== Testing Individual Sites ===")
    
    sites = ["mayoclinic.org", "medlineplus.gov", "nih.gov", "who.int", "cdc.gov"]
    
    for site in sites:
        print(f"\nTesting site: {site}")
        
        params = {
            "engine": "google",
            "q": "Diabetes medical information health",
            "api_key": api_key,
            "num": "5",
            "as_sitesearch": site,
            "safe": "active"
        }
        
        try:
            results = serpapi.search(params)
            print_results(results)
        except Exception as e:
            print(f"Error: {e}")

def test_without_site_restriction():
    """Test without any site restriction."""
    api_key = load_api_key()
    
    print("\n=== Testing Without Site Restriction ===")
    
    params = {
        "engine": "google",
        "q": "Diabetes medical information health",
        "api_key": api_key,
        "num": "5",
        "safe": "active"
    }
    
    print(f"Query: {params['q']}")
    
    try:
        results = serpapi.search(params)
        print_results(results)
    except Exception as e:
        print(f"Error: {e}")

def print_results(results):
    """Print the search results in a readable format."""
    if "organic_results" in results and results["organic_results"]:
        print(f"Found {len(results['organic_results'])} results:")
        for i, result in enumerate(results["organic_results"], 1):
            print(f"{i}. {result.get('title', 'No title')}")
            print(f"   URL: {result.get('link', 'No link')}")
            print(f"   Snippet: {result.get('snippet', 'No snippet')[:100]}...")
    else:
        print("No organic results found.")
        print("Response data:")
        # Print the search information if available
        if "search_information" in results:
            print(f"Search information: {json.dumps(results['search_information'], indent=2)}")
        # Print any error message if available
        if "error" in results:
            print(f"Error: {results['error']}")

def main():
    """Main function to run all tests."""
    print("\nDiagnosing SerpAPI Issue")
    print("=======================")
    
    # Test the original query that's failing
    test_original_query()
    
    # Test using the site: operator in the query
    test_site_operator()
    
    # Test each site individually
    test_individual_sites()
    
    # Test without any site restriction
    test_without_site_restriction()
    
    print("\nAll tests completed.")

if __name__ == "__main__":
    main()

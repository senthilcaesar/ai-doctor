#!/usr/bin/env python3
"""
Setup script for SERP API integration with Virtual Doctor Assistant.
This script helps install the required packages and set up the SERP API integration.

Usage:
    python setup_serp_api.py

This script will:
1. Check if the required packages are installed
2. Install missing packages
3. Check if the SERP API key is configured
4. Test the SERP API integration
"""

import os
import sys
import subprocess
import toml
import importlib.util

def check_package_installed(package_name):
    """Check if a package is installed."""
    return importlib.util.find_spec(package_name) is not None

def install_package(package_name):
    """Install a package using pip."""
    print(f"Installing {package_name}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
    print(f"{package_name} installed successfully.")

def check_and_install_packages():
    """Check and install required packages."""
    required_packages = ["serpapi", "toml", "streamlit"]
    
    for package in required_packages:
        if not check_package_installed(package):
            print(f"{package} is not installed.")
            try:
                install_package(package)
            except Exception as e:
                print(f"Error installing {package}: {e}")
                print(f"Please install {package} manually using: pip install {package}")
                return False
    
    print("All required packages are installed.")
    return True

def check_serp_api_key():
    """Check if the SERP API key is configured."""
    secrets_path = os.path.join('.streamlit', 'secrets.toml')
    
    # Check if .streamlit directory exists
    if not os.path.exists('.streamlit'):
        print("Creating .streamlit directory...")
        os.makedirs('.streamlit')
    
    # Check if secrets.toml exists
    if not os.path.exists(secrets_path):
        print("Creating secrets.toml file...")
        with open(secrets_path, 'w') as f:
            f.write("# API keys for the Virtual Doctor Assistant\n\n")
            f.write("# SERP API key for search engine results\n")
            f.write("SERP_API_KEY = \"your-serp-api-key-here\"\n\n")
            f.write("# OpenAI API key for the main assistant functionality\n")
            f.write("OPENAI_API_KEY = \"your-openai-api-key-here\"\n\n")
        print(f"Created {secrets_path} file. Please edit it to add your API keys.")
        return False
    
    # Check if SERP API key is configured
    try:
        secrets = toml.load(secrets_path)
        serp_api_key = secrets.get('SERP_API_KEY')
        
        if not serp_api_key or serp_api_key == "your-serp-api-key-here":
            print(f"SERP API key not found in {secrets_path}.")
            print(f"Please edit {secrets_path} to add your SERP API key.")
            return False
        
        print("SERP API key is configured.")
        return True
    
    except Exception as e:
        print(f"Error checking SERP API key: {e}")
        return False

def test_serp_api():
    """Test the SERP API integration."""
    try:
        # Import the test script
        import test_serp_api
        
        # Run the test
        print("Testing SERP API integration...")
        test_serp_api.main()
        
        return True
    
    except Exception as e:
        print(f"Error testing SERP API integration: {e}")
        return False

def main():
    """Main function."""
    print("\nSetting up SERP API integration for Virtual Doctor Assistant")
    print("==========================================================\n")
    
    # Check and install required packages
    if not check_and_install_packages():
        print("\nFailed to install required packages. Please install them manually.")
        return
    
    # Check SERP API key
    if not check_serp_api_key():
        print("\nPlease configure your SERP API key and run this script again.")
        return
    
    # Ask if the user wants to test the SERP API integration
    test_api = input("\nDo you want to test the SERP API integration? (y/n): ")
    if test_api.lower() == 'y':
        if not test_serp_api():
            print("\nFailed to test SERP API integration. Please check your API key and try again.")
            return
    
    print("\nSERP API integration setup completed successfully.")
    print("You can now run the Virtual Doctor Assistant with SERP API integration:")
    print("  streamlit run app.py")

if __name__ == "__main__":
    main()

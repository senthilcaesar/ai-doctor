# SERP API Integration for Virtual Doctor Assistant

This document provides information about the SERP API integration with the Virtual Doctor Assistant application. The integration allows the assistant to access up-to-date medical information from the web, enhancing its responses with current research, treatment guidelines, and health news.

## Overview

The SERP (Search Engine Results Page) API integration enables the Virtual Doctor Assistant to:

1. Search for medical information from reputable sources
2. Retrieve the latest medical research and findings
3. Access current treatment guidelines and protocols
4. Find information about emerging health conditions and treatments
5. Stay updated with the latest health news and developments

## Setup Instructions

### 1. Automated Setup

The easiest way to set up the SERP API integration is to use the provided setup script:

```bash
python setup_serp_api.py
```

This script will:

1. Check if the required packages are installed and install any missing packages
2. Check if the SERP API key is configured in `.streamlit/secrets.toml`
3. Test the SERP API integration to ensure it's working correctly

### 2. Manual Setup

If you prefer to set up the integration manually, follow these steps:

#### 2.1. Get a SERP API Key

To use the SERP API integration, you need to obtain an API key from SerpApi:

1. Visit [SerpApi](https://serpapi.com/) and create an account
2. Navigate to your dashboard and obtain your API key
3. Add your API key to the `.streamlit/secrets.toml` file:

```toml
# SERP API key for search engine results
SERP_API_KEY = "your-serp-api-key-here"
```

#### 2.2. Install Required Packages

This integration uses the `serpapi` package, which should be installed via pip:

```bash
pip install serpapi
```

#### 2.3. Test the Integration

You can test the integration using the provided test script:

```bash
python test_serp_api.py
```

### 2. Usage Limits and Pricing

SerpApi offers different pricing tiers based on the number of searches:

- **Free Tier**: 100 searches per month
- **Paid Tiers**: Starting from $50/month for 5,000 searches

For the latest pricing information, visit the [SerpApi Pricing Page](https://serpapi.com/pricing).

## How It Works

The SERP API integration works as follows:

1. When a user asks a medical question, the Virtual Doctor Assistant first provides a response based on its built-in knowledge.
2. The system then analyzes the response to determine if it could benefit from supplementary information from the web.
3. If appropriate, the system uses the SERP API to search for relevant medical information from reputable sources.
4. The search results are filtered to prioritize trusted medical sources (e.g., Mayo Clinic, NIH, CDC, WHO).
5. The relevant information is added to the assistant's response, clearly marked as coming from external sources.
6. Appropriate medical disclaimers are included with the supplementary information.

## When SERP API Is Used

The system intelligently determines when to enhance responses with SERP data based on:

1. **Uncertainty in the response**: When the assistant expresses uncertainty or indicates limited information
2. **Recency-related queries**: When the user asks about recent developments, latest research, or new treatments
3. **Specific medical queries**: When the user asks detailed questions about specific medical conditions or treatments
4. **Short responses**: When the assistant's initial response is relatively brief, suggesting limited information

## Features

### Medical Information Search

The `search_medical_info` function searches for medical information related to a specific query:

```python
search_results = serp_service.search_medical_info("diabetes treatment guidelines")
```

### Medical News Retrieval

The `get_medical_news` function retrieves the latest news on a specific medical topic:

```python
news_results = serp_service.get_medical_news("covid-19 research")
```

### Source Validation

The system validates sources to prioritize reputable medical websites:

```python
is_trusted = serp_service.validate_medical_source("mayoclinic.org/diseases-conditions/diabetes/...")
```

### Medical Disclaimers

The system generates appropriate medical disclaimers based on the content of search results:

```python
disclaimer = serp_service.generate_medical_disclaimer(search_results)
```

## Customization

You can customize the SERP API integration by modifying the following files:

- `serp_service.py`: Contains the core SERP API service class
- `serp_utils.py`: Contains utility functions for enhancing responses with SERP data

### Trusted Domains

You can modify the list of trusted medical domains in the `validate_medical_source` function in `serp_service.py`:

```python
trusted_domains = [
    "nih.gov", "cdc.gov", "who.int", "mayoclinic.org", "clevelandclinic.org",
    # Add or remove domains as needed
]
```

### Search Parameters

You can customize the search parameters in the `search_medical_info` function in `serp_service.py`:

```python
params = {
    "engine": "google",
    "q": medical_query,
    "api_key": self.api_key,
    "num": num_results,
    # Modify parameters as needed
    "as_sitesearch": "mayoclinic.org,medlineplus.gov,nih.gov,who.int,cdc.gov",
    "safe": "active"
}
```

## Testing the Integration

A test script is provided to verify that the SERP API integration is working correctly:

```bash
python test_serp_api.py
```

This script performs the following tests:

1. **Medical Information Search**: Tests searching for medical information on various topics
2. **Medical News Retrieval**: Tests retrieving the latest news on medical topics
3. **Source Validation**: Tests the validation of medical sources

The test script will output the results of each test, including:

- Search results for medical information
- Latest medical news
- Validation of trusted medical sources
- Generated medical disclaimers

### Example Output

```
Testing SERP API Integration for Virtual Doctor Assistant
--------------------------------------------------------

================================================================================
SEARCHING FOR: diabetes treatment guidelines
================================================================================

1. ✓ Treatment & Management | ADA - American Diabetes Association
   Learn about the treatment options for diabetes, including medications, meal planning, and blood glucose monitoring.
   Source: https://diabetes.org/diabetes/treatment-care

2. ✓ Standards of Care | ADA - American Diabetes Association
   The Standards of Medical Care in Diabetes includes all of ADA's current clinical practice recommendations and is intended to provide clinicians, patients, ...
   Source: https://diabetes.org/diabetes/treatment-care/standards-of-care

3. ✓ Type 2 Diabetes - Diagnosis and treatment - Mayo Clinic
   Treatment for type 2 diabetes requires a lifelong commitment to: Blood sugar monitoring; Healthy eating; Regular exercise; Weight loss; Possibly, diabetes ...
   Source: https://www.mayoclinic.org/diseases-conditions/type-2-diabetes/diagnosis-treatment/drc-20351199

Disclaimer: IMPORTANT: Treatment information should be discussed with a healthcare provider. Information from web searches is not a substitute for professional medical advice, diagnosis, or treatment.
```

## Troubleshooting

### API Key Issues

If you encounter issues with the SERP API key:

1. Verify that the API key is correctly added to the `.streamlit/secrets.toml` file
2. Check that the API key is active and has not expired
3. Ensure you have not exceeded your API usage limits
4. Run the test script to verify that the API key is working correctly

If you see a "401 Client Error: Unauthorized" error with the message "Invalid API key", this means your API key is not valid or has expired. You need to:

1. Visit [SerpApi](https://serpapi.com/) and log in to your account
2. Navigate to your dashboard and check your API key status
3. If your API key has expired, you may need to upgrade your plan or create a new API key
4. Update the API key in `.streamlit/secrets.toml`

Example error message:

```
Request failed with status code: 401
Response: {
  "error": "Invalid API key. Your API key should be here: https://serpapi.com/manage-api-key"
}
```

### Rate Limiting

The SERP API integration includes rate limiting to avoid exceeding API limits. If you encounter rate limiting issues:

1. Adjust the `rate_limit` parameter in the `SerpService` initialization
2. Consider upgrading to a higher tier with SerpApi for increased limits

### No Results

If the SERP API is not returning results:

1. Check your internet connection
2. Verify that the search query is properly formatted
3. Try a different search query to see if the issue persists
4. Check the SerpApi status page for any service disruptions

## Privacy and Security

The SERP API integration is designed with privacy and security in mind:

1. No patient identifiable information is included in search queries
2. All API calls use HTTPS to ensure data in transit is encrypted
3. Search logs are stored separately from patient conversation logs
4. Content filtering is implemented to prevent inappropriate content

## Feedback and Improvement

The SERP API integration is continuously improved based on user feedback. If you have suggestions or encounter issues, please provide feedback through the application's feedback system.

import os
import json
import time
from functools import lru_cache
import serpapi

class SerpService:
    """
    Service for accessing search engine results via SERP API.
    Provides methods for searching medical information and retrieving medical news.
    """
    
    def __init__(self, api_key=None, rate_limit=5):
        """
        Initialize the SERP service with API key and rate limiting.
        
        Args:
            api_key (str, optional): The SERP API key. If not provided, will try to get from environment.
            rate_limit (int, optional): Maximum number of requests per minute. Defaults to 5.
        """
        self.api_key = api_key or os.environ.get("SERP_API_KEY")
        if not self.api_key:
            raise ValueError("SERP API key is required")
        
        self.rate_limit = rate_limit
        self.last_request_time = 0
    
    def _rate_limit(self):
        """Implement rate limiting to avoid exceeding API limits."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        # If less than rate limit seconds have passed
        if time_since_last < (60 / self.rate_limit):
            sleep_time = (60 / self.rate_limit) - time_since_last
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    @lru_cache(maxsize=100)
    def search_medical_info(self, query, num_results=5):
        """
        Search for medical information using SERP API.
        Results are cached to reduce API calls for identical queries.
        
        Args:
            query (str): The search query
            num_results (int, optional): Number of results to return. Defaults to 5.
            
        Returns:
            list: List of search results with title, link, and snippet
        """
        # Apply rate limiting
        self._rate_limit()
        
        # Add medical context to the query
        medical_query = f"{query} medical information health"
        
        # Create site restriction using site: operator
        sites = ["mayoclinic.org", "medlineplus.gov", "nih.gov", "who.int", "cdc.gov"]
        site_query = " OR ".join([f"site:{site}" for site in sites])
        full_query = f"{medical_query} ({site_query})"
        
        # SerpAPI implementation
        params = {
            "engine": "google",
            "q": full_query,
            "api_key": self.api_key,
            "num": num_results,
            "safe": "active"  # Safe search to filter inappropriate content
        }
        
        results = serpapi.search(params)
        
        # Extract and format the organic results
        formatted_results = []
        if "organic_results" in results:
            for result in results["organic_results"][:num_results]:
                # Check if the source is a reputable medical source
                url = result.get("link", "")
                is_trusted = self.validate_medical_source(url)
                
                formatted_results.append({
                    "title": result.get("title", ""),
                    "link": url,
                    "snippet": result.get("snippet", ""),
                    "source": "SERP API",
                    "is_trusted": is_trusted
                })
        
        return formatted_results
    
    @lru_cache(maxsize=50)
    def get_medical_news(self, topic, num_results=3):
        """
        Get latest medical news on a specific topic.
        Results are cached to reduce API calls for identical queries.
        
        Args:
            topic (str): The medical topic to search for
            num_results (int, optional): Number of news results to return. Defaults to 3.
            
        Returns:
            list: List of news results
        """
        # Apply rate limiting
        self._rate_limit()
        
        # Create query with medical news context
        query = f"{topic} latest medical research news"
        
        # Create site restriction using site: operator for medical news sources
        news_sites = ["nih.gov", "medlineplus.gov", "mayoclinic.org", "webmd.com", 
                      "medicalnewstoday.com", "healthline.com", "nejm.org", "jamanetwork.com"]
        site_query = " OR ".join([f"site:{site}" for site in news_sites])
        full_query = f"{query} ({site_query})"
        
        params = {
            "engine": "google",
            "q": full_query,
            "api_key": self.api_key,
            "num": num_results,
            "tbm": "nws",  # News search
            "tbs": "qdr:m"  # Last month
        }
        
        results = serpapi.search(params)
        
        # Extract and format the news results
        news_results = []
        if "news_results" in results:
            for result in results["news_results"][:num_results]:
                # Check if the source is a reputable medical source
                url = result.get("link", "")
                is_trusted = self.validate_medical_source(url)
                
                news_results.append({
                    "title": result.get("title", ""),
                    "link": url,
                    "snippet": result.get("snippet", ""),
                    "source": result.get("source", ""),
                    "date": result.get("date", ""),
                    "is_trusted": is_trusted
                })
        
        return news_results
    
    def validate_medical_source(self, url):
        """
        Validate if a URL is from a reputable medical source.
        
        Args:
            url (str): The URL to validate
            
        Returns:
            bool: True if the URL is from a reputable medical source, False otherwise
        """
        trusted_domains = [
            "nih.gov", "cdc.gov", "who.int", "mayoclinic.org", "clevelandclinic.org",
            "hopkinsmedicine.org", "health.harvard.edu", "medlineplus.gov", "webmd.com",
            "healthline.com", "medicalnewstoday.com", "nejm.org", "jamanetwork.com",
            "thelancet.com", "bmj.com", "nature.com", "science.org", "cell.com",
            "pubmed.ncbi.nlm.nih.gov", "uptodate.com", "aafp.org", "aap.org", "heart.org",
            "cancer.gov", "cancer.org", "diabetes.org", "psychiatry.org", "acog.org"
        ]
        
        return any(domain in url.lower() for domain in trusted_domains)
    
    def generate_medical_disclaimer(self, search_results):
        """
        Generate appropriate disclaimers based on search results.
        
        Args:
            search_results (list): List of search results
            
        Returns:
            str: Disclaimer text
        """
        disclaimer = "IMPORTANT: "
        
        # Check if results contain recent studies
        contains_studies = any("study" in result.get("snippet", "").lower() for result in search_results)
        if contains_studies:
            disclaimer += "The information about studies may be preliminary and not yet peer-reviewed. "
        
        # Check if results contain treatments
        contains_treatments = any("treatment" in result.get("snippet", "").lower() for result in search_results)
        if contains_treatments:
            disclaimer += "Treatment information should be discussed with a healthcare provider. "
        
        # Add general disclaimer
        disclaimer += "Information from web searches is not a substitute for professional medical advice, diagnosis, or treatment."
        
        return disclaimer

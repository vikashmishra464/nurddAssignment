import sys
import requests
import json
import os
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

# This is a placeholder for your Gemini API key.
# You should get this from your environment variables or a secure file.
# Do NOT hardcode your key here in a production environment.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# The URL for the Gemini API
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent"

def enhance_description(description):
    """
    Uses the Gemini API to enhance a given text description for better readability.
    
    Args:
        description (str): The text description to enhance.
        
    Returns:
        str: The enhanced description or the original description if the API call fails.
    """
    if not GEMINI_API_KEY:
        return description + " (Note: API key missing, description not enhanced.)"

    try:
        headers = {
            "Content-Type": "application/json"
        }
        
        # The prompt to send to the Gemini API
        prompt_text = (
            "Enhance the following website description for better readability and clarity. "
            "Keep the tone professional but easy to understand. "
            "Ensure the output is a single paragraph. "
            f"Description: \"{description}\""
        )
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt_text}
                    ]
                }
            ]
        }
        
        params = {
            "key": GEMINI_API_KEY
        }

        response = requests.post(GEMINI_API_URL, headers=headers, json=payload, params=params, timeout=15)
        response.raise_for_status()
        
        result = response.json()
        
        # Extract the enhanced text from the API response
        enhanced_text = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text")
        
        if enhanced_text:
            return enhanced_text.strip()
        else:
            return description
            
    except RequestException as e:
        print(f"Error calling Gemini API: {e}", file=sys.stderr)
        return description + " (Note: Gemini API call failed, description not enhanced.)"
    except (json.JSONDecodeError, IndexError) as e:
        print(f"Error parsing Gemini API response: {e}", file=sys.stderr)
        return description + " (Note: Gemini API response parsing failed, description not enhanced.)"


def scrape(url):
    """
    Scrapes a website for its brand name and description, then enhances the description.
    
    Args:
        url (str): The URL of the website to scrape.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Scrape brand name
        brand = (
            soup.find("meta", property="og:site_name") and soup.find("meta", property="og:site_name").get("content")
        ) or (soup.title.string if soup.title else None) or url

        # Scrape description
        description = (
            soup.find("meta", attrs={"name": "description"}) and soup.find("meta", attrs={"name": "description"}).get("content")
        ) or (
            soup.find("meta", property="og:description") and soup.find("meta", property="og:description").get("content")
        ) or (
            soup.find("p").get_text(strip=True) if soup.find("p") else "No description found"
        )
        
        # Enhance the scraped description using the Gemini API
        enhanced_description = enhance_description(description)

        result = {
            "brandname": brand,
            "description": enhanced_description
        }
        
        # Print the final result as a JSON string
        print(json.dumps(result))
    except Exception as e:
        # Catch and print any errors in JSON format
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    try:
        url = sys.argv[1]
        scrape(url)
    except IndexError:
        print(json.dumps({"error": "No URL provided. Usage: python scraper.py <url>"}))

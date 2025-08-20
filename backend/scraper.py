import sys
import requests
import json
import os
import random
import time
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent"

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/109.0.1518.78',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/108.0'
]

def enhance_description(description):
    if not GEMINI_API_KEY:
        return description + " (Note: API key missing, description not enhanced.)"

    try:
        headers = {
            "Content-Type": "application/json"
        }
        
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
        
        enhanced_text = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text")
        
        if enhanced_text:
            return enhanced_text.strip()
        else:
            return description
            
    except RequestException as e:
        print(f"Error calling Gemini API: {e} - Status Code: {e.response.status_code if e.response else 'N/A'}", file=sys.stderr)
        return description + " (Note: Gemini API call failed, description not enhanced.)"
    except (json.JSONDecodeError, IndexError) as e:
        print(f"Error parsing Gemini API response: {e}", file=sys.stderr)
        return description + " (Note: Gemini API response parsing failed, description not enhanced.)"

def scrape(url):
    try:
        # Add a random delay before the request to mimic human behavior
        sleep_time = random.uniform(2, 5)
        time.sleep(sleep_time)
        
        # Use a random User-Agent from the list
        headers = {
            'User-Agent': random.choice(USER_AGENTS)
        }
        
        # Pass headers to the requests.get() method
        response = requests.get(url, headers=headers, timeout=10)
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
        
        enhanced_description = enhance_description(description)

        result = {
            "brandname": brand,
            "description": enhanced_description
        }
        
        print(json.dumps(result))
    except RequestException as e:
        # Catch specific HTTP errors and provide more detail
        error_message = f"HTTP Error: {e.response.status_code} - {e.response.reason}" if e.response else str(e)
        print(json.dumps({"error": f"Failed to scrape {url}. Reason: {error_message}"}))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    try:
        url = sys.argv[1]
        scrape(url)
    except IndexError:
        print(json.dumps({"error": "No URL provided. Usage: python scraper.py <url>"}))
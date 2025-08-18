import sys
import requests
from bs4 import BeautifulSoup
import json

def scrape(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract brand name
        brand = (
            soup.find("meta", property="og:site_name") and soup.find("meta", property="og:site_name").get("content")
        ) or (soup.title.string if soup.title else None) or url

        # Extract description
        description = (
            soup.find("meta", attrs={"name": "description"}) and soup.find("meta", attrs={"name": "description"}).get("content")
        ) or (
            soup.find("meta", property="og:description") and soup.find("meta", property="og:description").get("content")
        ) or (
            soup.find("p").get_text(strip=True) if soup.find("p") else "No description found"
        )

        result = {
            "brandname": brand,
            "description": description
        }
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    url = sys.argv[1]  # Get URL from command line
    scrape(url)

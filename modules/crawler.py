import requests
from bs4 import BeautifulSoup

def fetch_page_content(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            return response.text
    except requests.exceptions.RequestException:
        return None
    return None

import requests
from bs4 import BeautifulSoup
import time

def google_dork(query):
    headers = {"User-Agent": "Mozilla/5.0"}
    url = f"https://www.google.com/search?q={query}&num=10"
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            results = []
            for g in soup.find_all('div', class_='tF2Cxc'):
                link = g.find('a')['href']
                results.append(link)
            return results
    except requests.exceptions.RequestException:
        return []
    
    return []

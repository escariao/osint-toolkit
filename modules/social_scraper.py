import requests
from bs4 import BeautifulSoup

def scrape_social_profiles(domain):
    """
    Faz scraping no Google para encontrar perfis sociais relacionados ao domínio fornecido.
    Retorna um dicionário com os links encontrados.
    """
    query = f'"{domain}" site:linkedin.com OR site:twitter.com OR site:facebook.com OR site:instagram.com'
    google_search_url = f"https://www.google.com/search?q={query}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    response = requests.get(google_search_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        links = [a["href"] for a in soup.find_all("a", href=True) if "url?q=" in a["href"]]

        social_profiles = {}
        for link in links:
            if "facebook.com" in link:
                social_profiles["Facebook"] = link
            elif "twitter.com" in link:
                social_profiles["Twitter"] = link
            elif "linkedin.com" in link:
                social_profiles["LinkedIn"] = link
            elif "instagram.com" in link:
                social_profiles["Instagram"] = link

        print("Perfis sociais encontrados:", social_profiles)  # Debug
        return social_profiles
    else:
        return {}

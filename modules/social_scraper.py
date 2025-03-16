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

    try:
        response = requests.get(google_search_url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        links = []
        for a in soup.find_all("a", href=True):
            url = a["href"]
            if "url?q=" in url and not "webcache" in url:
                real_url = url.split("url?q=")[1].split("&")[0]
                if any(social in real_url for social in ["linkedin.com", "twitter.com", "facebook.com", "instagram.com"]):
                    links.append(real_url)

        social_profiles = {
            "Facebook": next((link for link in links if "facebook.com" in link), "Não encontrado"),
            "Twitter": next((link for link in links if "twitter.com" in link), "Não encontrado"),
            "LinkedIn": next((link for link in links if "linkedin.com" in link), "Não encontrado"),
            "Instagram": next((link for link in links if "instagram.com" in link), "Não encontrado"),
        }

        print("Perfis sociais encontrados:", social_profiles)  # Debug
        return social_profiles

    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar perfis sociais: {e}")
        return {}

import requests
import re
from bs4 import BeautifulSoup

def scrape_social_profiles(domain):
    """
    Faz scraping no Google e na própria página do domínio para encontrar perfis sociais.
    Retorna um dicionário com os links encontrados.
    """
    social_profiles = {
        "Facebook": "Não encontrado",
        "Twitter": "Não encontrado",
        "LinkedIn": "Não encontrado",
        "Instagram": "Não encontrado",
    }

    # 🔹 1️⃣ Buscar links sociais na própria página do site
    try:
        response = requests.get(f"https://{domain}", timeout=10, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        })
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if "facebook.com" in href:
                    social_profiles["Facebook"] = href
                if "twitter.com" in href or "x.com" in href:
                    social_profiles["Twitter"] = href
                if "linkedin.com" in href:
                    social_profiles["LinkedIn"] = href
                if "instagram.com" in href:
                    social_profiles["Instagram"] = href
    except Exception as e:
        print(f"Erro ao buscar na própria página: {e}")

    # 🔹 2️⃣ Tentar buscar no Google se não encontrar na página
    if "Não encontrado" in social_profiles.values():
        query = f'"{domain}" site:linkedin.com OR site:twitter.com OR site:facebook.com OR site:instagram.com'
        google_search_url = f"https://www.google.com/search?q={query}"

        try:
            response = requests.get(google_search_url, timeout=10, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
            })
            soup = BeautifulSoup(response.text, "html.parser")

            # 🔍 Regex para encontrar links corretos
            links = re.findall(r"https?://(www\.)?(facebook|twitter|linkedin|instagram)\.com/[^\s\"']+", response.text)

            for link in links:
                if "facebook.com" in link:
                    social_profiles["Facebook"] = link
                if "twitter.com" in link or "x.com" in link:
                    social_profiles["Twitter"] = link
                if "linkedin.com" in link:
                    social_profiles["LinkedIn"] = link
                if "instagram.com" in link:
                    social_profiles["Instagram"] = link

        except Exception as e:
            print(f"Erro ao buscar no Google: {e}")

    print("Perfis sociais encontrados:", social_profiles)  # Debug
    return social_profiles

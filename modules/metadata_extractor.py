from bs4 import BeautifulSoup
import requests

def extract_metadata(domain):
    url = f"http://{domain}"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.RequestException:
        return {"title": "Erro ao acessar", "description": "Erro ao acessar", "keywords": "Erro ao acessar"}
    
    soup = BeautifulSoup(response.text, "html.parser")

    # Extraindo metadados de várias formas
    metadata = {
        "title": soup.title.string.strip() if soup.title else "N/A",
        "description": "N/A",
        "keywords": "N/A"
    }

    # Verificar meta description
    desc_tag = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
    if desc_tag and "content" in desc_tag.attrs:
        metadata["description"] = desc_tag["content"].strip()

    # Verificar meta keywords
    keywords_tag = soup.find("meta", attrs={"name": "keywords"})
    if keywords_tag and "content" in keywords_tag.attrs:
        metadata["keywords"] = keywords_tag["content"].strip()

    print("Metadados extraídos:", metadata)  # Log para verificar saída

    return metadata

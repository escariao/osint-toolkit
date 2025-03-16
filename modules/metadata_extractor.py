from bs4 import BeautifulSoup

def extract_metadata(html_content):
    """
    Extrai metadados de uma página HTML, incluindo título, descrição e palavras-chave.
    Verifica outras variações de meta tags comuns.
    """
    if not html_content:
        return {"title": "N/A", "description": "N/A", "keywords": "N/A"}

    soup = BeautifulSoup(html_content, "html.parser")

    metadata = {
        "title": soup.title.string.strip() if soup.title and soup.title.string else "N/A",
        "description": "N/A",
        "keywords": "N/A"
    }

    # Verifica múltiplas variações de meta description
    description_tags = [
        soup.find("meta", attrs={"name": "description"}),
        soup.find("meta", attrs={"property": "og:description"}),
        soup.find("meta", attrs={"name": "twitter:description"})
    ]
    
    for tag in description_tags:
        if tag and tag.has_attr("content"):
            metadata["description"] = tag["content"].strip()
            break  # Usa a primeira encontrada

    # Verifica múltiplas variações de meta keywords
    keywords_tags = [
        soup.find("meta", attrs={"name": "keywords"}),
        soup.find("meta", attrs={"property": "og:keywords"}),
    ]
    
    for tag in keywords_tags:
        if tag and tag.has_attr("content"):
            metadata["keywords"] = tag["content"].strip()
            break

    return metadata

from bs4 import BeautifulSoup

def extract_metadata(html_content):
    if not html_content:
        return {"title": "N/A", "description": "N/A", "keywords": "N/A"}

    soup = BeautifulSoup(html_content, "html.parser")

    metadata = {
        "title": soup.title.string.strip() if soup.title and soup.title.string else "N/A",
        "description": "N/A",
        "keywords": "N/A"
    }

    description_tags = [
        soup.find("meta", attrs={"name": "description"}),
        soup.find("meta", attrs={"property": "og:description"}),
        soup.find("meta", attrs={"name": "twitter:description"})
    ]
    
    for tag in description_tags:
        if tag and tag.has_attr("content"):
            metadata["description"] = tag["content"].strip()
            break

    keywords_tags = [
        soup.find("meta", attrs={"name": "keywords"}),
        soup.find("meta", attrs={"property": "og:keywords"}),
    ]
    
    for tag in keywords_tags:
        if tag and tag.has_attr("content"):
            metadata["keywords"] = tag["content"].strip()
            break

    # Debug: imprimir saída
    print("Metadados extraídos:", metadata)

    return metadata

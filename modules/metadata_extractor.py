# modules/metadata_extractor.py

from bs4 import BeautifulSoup

def extract_metadata(html_content):
    """
    Extrai metadados de uma página HTML, como título, descrição e palavras-chave.

    :param html_content: Conteúdo HTML da página.
    :return: Dicionário contendo os metadados extraídos.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    
    metadata = {
        "title": soup.title.string if soup.title else "N/A",
        "description": "N/A",
        "keywords": "N/A"
    }

    # Pega a meta tag description
    meta_description = soup.find("meta", attrs={"name": "description"})
    if meta_description and "content" in meta_description.attrs:
        metadata["description"] = meta_description["content"]

    # Pega a meta tag keywords
    meta_keywords = soup.find("meta", attrs={"name": "keywords"})
    if meta_keywords and "content" in meta_keywords.attrs:
        metadata["keywords"] = meta_keywords["content"]

    return metadata

if __name__ == "__main__":
    # Teste rápido
    sample_html = """
        <html>
            <head>
                <title>Exemplo de Página</title>
                <meta name="description" content="Esta é uma descrição de exemplo.">
                <meta name="keywords" content="OSINT, segurança, metadados">
            </head>
            <body>
                <h1>Bem-vindo!</h1>
            </body>
        </html>
    """
    found_metadata = extract_metadata(sample_html)
    print("Metadados extraídos:", found_metadata)

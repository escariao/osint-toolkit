# modules/link_extractor.py

import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup

def extract_links(html_content, base_url):
    """
    Extrai links de uma página HTML.

    :param html_content: Conteúdo HTML da página.
    :param base_url: URL base para resolver links relativos.
    :return: Lista de links extraídos.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    links = set()

    for tag in soup.find_all("a", href=True):
        href = tag["href"]
        full_url = urljoin(base_url, href)  # Resolve links relativos
        links.add(full_url)

    return list(links)

if __name__ == "__main__":
    # Teste rápido
    sample_html = """
        <html>
            <body>
                <a href="http://example.com/page1">Link 1</a>
                <a href="/page2">Link 2</a>
            </body>
        </html>
    """
    base_url = "http://example.com"
    found_links = extract_links(sample_html, base_url)
    print("Links encontrados:", found_links)

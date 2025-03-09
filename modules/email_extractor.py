import re
import requests
from bs4 import BeautifulSoup

def extract_emails(domain):
    """
    Extrai emails da página principal do domínio e suas páginas internas.
    
    :param domain: O domínio a ser analisado.
    :return: Lista de emails encontrados.
    """
    emails = set()
    try:
        url = f"http://{domain}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            emails.update(find_emails(response.text))

            # Procurar emails em links internos da página
            soup = BeautifulSoup(response.text, "html.parser")
            links = {a["href"] for a in soup.find_all("a", href=True) if domain in a["href"]}

            for link in links:
                if len(emails) >= 10:  # Evita sobrecarga no servidor
                    break
                try:
                    sub_response = requests.get(link, timeout=5)
                    if sub_response.status_code == 200:
                        emails.update(find_emails(sub_response.text))
                except requests.RequestException:
                    pass

    except requests.RequestException:
        pass

    return list(emails) if emails else ["Nenhum email encontrado."]

def find_emails(html_content):
    """
    Aplica regex para encontrar emails no conteúdo HTML.
    
    :param html_content: Conteúdo HTML a ser analisado.
    :return: Lista de emails encontrados.
    """
    email_regex = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    return set(re.findall(email_regex, html_content))

if __name__ == "__main__":
    # Teste rápido
    test_domain = "example.com"
    found_emails = extract_emails(test_domain)
    print("Emails encontrados:", found_emails)

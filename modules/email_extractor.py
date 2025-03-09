import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def extract_emails(domain):
    """
    Extrai emails apenas do domínio pesquisado.

    :param domain: O domínio a ser analisado.
    :return: Lista de emails filtrados.
    """
    emails = set()
    try:
        url = f"http://{domain}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            emails.update(find_emails(response.text, domain))

            # Procurar emails em links internos da página
            soup = BeautifulSoup(response.text, "html.parser")
            links = {a["href"] for a in soup.find_all("a", href=True) if domain in a["href"]}

            for link in links:
                if len(emails) >= 10:  # Evita sobrecarga no servidor
                    break
                try:
                    sub_response = requests.get(link, timeout=5)
                    if sub_response.status_code == 200:
                        emails.update(find_emails(sub_response.text, domain))
                except requests.RequestException:
                    pass

    except requests.RequestException:
        pass

    return list(emails) if emails else ["Nenhum email encontrado."]

def find_emails(html_content, domain):
    """
    Aplica regex para encontrar emails e filtra apenas do domínio pesquisado.

    :param html_content: Conteúdo HTML a ser analisado.
    :param domain: O domínio pesquisado.
    :return: Lista de emails filtrados.
    """
    email_regex = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    all_emails = set(re.findall(email_regex, html_content))

    # Filtrar apenas emails do domínio pesquisado
    valid_emails = {email for email in all_emails if email.endswith(f"@{domain}")}

    return valid_emails

if __name__ == "__main__":
    # Teste rápido
    test_domain = "google.com"
    found_emails = extract_emails(test_domain)
    print("Emails encontrados:", found_emails)

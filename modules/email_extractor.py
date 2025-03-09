import re
import requests
from bs4 import BeautifulSoup

def extract_emails(domain):
    """
    Extrai e-mails de um domínio, incluindo formas ofuscadas.
    """
    emails = set()
    
    try:
        # Faz a requisição para a página principal do domínio
        response = requests.get(f"http://{domain}", timeout=5)
        response.raise_for_status()
        html_content = response.text
    except requests.RequestException:
        return []
    
    # Expressões regulares para capturar e-mails
    email_patterns = [
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",  # Padrão tradicional
        r"[a-zA-Z0-9._%+-]+\s?\(at\)\s?[a-zA-Z0-9.-]+\s?\(dot\)\s?[a-zA-Z]{2,}",  # E-mails ofuscados
        r"[a-zA-Z0-9._%+-]+\s?\[at\]\s?[a-zA-Z0-9.-]+\s?\[dot\]\s?[a-zA-Z]{2,}"  # Outra variação de ofuscação
    ]
    
    for pattern in email_patterns:
        matches = re.findall(pattern, html_content, re.IGNORECASE)
        for match in matches:
            emails.add(match)
    
    # Removendo URLs incorretamente capturadas
    filtered_emails = {email for email in emails if "@" in email and "." in email.split("@")[-1]}
    
    return list(filtered_emails)

if __name__ == "__main__":
    # Teste rápido
    domain = "example.com"
    found_emails = extract_emails(domain)
    print("E-mails encontrados:", found_emails)

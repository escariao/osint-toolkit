import re
import requests
import dns.resolver
from bs4 import BeautifulSoup

def extract_emails_from_text(text):
    """
    Extrai emails de um texto, incluindo e-mails ofuscados como "exemplo[at]dominio[dot]com".
    """
    if not text:
        return []
    
    # Regex aprimorada para capturar variações comuns de e-mails
    email_regex = re.compile(
        r'([a-zA-Z0-9_.+-]+\s?(@|\[at\]\s?)\s?[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)',
        re.IGNORECASE
    )
    matches = email_regex.findall(text)
    
    extracted_emails = set()
    for match in matches:
        email = match[0].replace("[at]", "@").replace("[dot]", ".").replace(" ", "")
        extracted_emails.add(email)
    
    return list(extracted_emails)

def extract_emails_from_html(html_content):
    """
    Extrai emails do conteúdo HTML da página, buscando no corpo e em meta tags.
    """
    if not html_content:
        return []
    
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text() + " " + " ".join([tag["content"] for tag in soup.find_all("meta", content=True)])
    return extract_emails_from_text(text)

def extract_emails_from_dns(domain):
    """
    Extrai emails dos registros TXT do DNS, onde algumas empresas escondem contatos.
    """
    emails = set()
    try:
        txt_records = dns.resolver.resolve(domain, 'TXT')
        for record in txt_records:
            emails.update(extract_emails_from_text(record.to_text()))
    except Exception:
        pass
    return list(emails)

def extract_emails(domain):
    """
    Coleta e-mails do HTML da página e dos registros DNS.
    """
    emails = set()
    
    # Tenta buscar no HTML da página principal
    try:
        response = requests.get(f"http://{domain}", timeout=5)
        if response.status_code == 200:
            emails.update(extract_emails_from_html(response.text))
    except requests.RequestException:
        pass
    
    # Tenta buscar nos registros DNS
    emails.update(extract_emails_from_dns(domain))
    
    return list(emails)

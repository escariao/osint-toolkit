import re
import requests
import dns.resolver
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def extract_emails_from_html(html_content):
    """
    Extrai e-mails de um conteúdo HTML, incluindo formatos ofuscados.
    """
    email_patterns = [
        r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',  # E-mails normais
        r'([a-zA-Z0-9_.+-]+)\s*\[at\]\s*([a-zA-Z0-9-]+)\s*\[dot\]\s*([a-zA-Z0-9-.]+)',  # e-mails ofuscados com [at] e [dot]
        r'([a-zA-Z0-9_.+-]+)\s*\(at\)\s*([a-zA-Z0-9-]+)\s*\(dot\)\s*([a-zA-Z0-9-.]+)'
    ]
    
    emails = set()
    for pattern in email_patterns:
        matches = re.findall(pattern, html_content, re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                email = f"{match[0]}@{match[1]}.{match[2]}"
            else:
                email = match
            emails.add(email)
    
    return list(emails)

def extract_emails_from_dns(domain):
    """
    Extrai e-mails dos registros TXT do DNS.
    """
    emails = set()
    try:
        txt_records = dns.resolver.resolve(domain, 'TXT')
        for record in txt_records:
            emails.update(re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', record.to_text()))
    except:
        pass
    return list(emails)

def crawl_additional_pages(domain):
    """
    Tenta encontrar e-mails em páginas comuns como /contact, /about, /support.
    """
    common_pages = ["contact", "about", "support", "help", "info"]
    emails = set()
    for page in common_pages:
        url = urljoin(f"http://{domain}", page)
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                emails.update(extract_emails_from_html(response.text))
        except:
            pass
    return list(emails)

def extract_emails(domain):
    """
    Extrai e-mails de um domínio combinando múltiplas fontes.
    """
    emails = set()
    
    # Tenta extrair do HTML principal
    try:
        response = requests.get(f"http://{domain}", timeout=5)
        if response.status_code == 200:
            emails.update(extract_emails_from_html(response.text))
    except:
        pass
    
    # Tenta extrair do DNS
    emails.update(extract_emails_from_dns(domain))
    
    # Tenta extrair de páginas adicionais
    emails.update(crawl_additional_pages(domain))
    
    return list(emails)

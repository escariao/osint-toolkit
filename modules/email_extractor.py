import re
import requests
import dns.resolver
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def extract_emails_from_text(text):
    """
    Extrai emails, incluindo formatos ofuscados comuns.
    """
    email_patterns = [
        r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',  # Emails normais
        r'[a-zA-Z0-9._%+-]+\s*\[at\]\s*[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',  # contato [at] google.com
        r'[a-zA-Z0-9._%+-]+\s*\(at\)\s*[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',  # contato(at)google.com
        r'[a-zA-Z0-9._%+-]+\s*\[arroba\]\s*[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',  # contato [arroba] google.com
        r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\s*\[dot\]\s*[a-zA-Z]{2,}',  # contato@google[dot]com
    ]
    
    emails = set()
    for pattern in email_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for email in matches:
            email = email.replace("[at]", "@").replace("(at)", "@").replace("[arroba]", "@").replace("[dot]", ".")
            emails.add(email)
    
    return list(emails)

def extract_emails_from_dns(domain):
    """
    Extrai emails de registros TXT do DNS (SPF, DKIM, DMARC).
    """
    emails = set()
    try:
        txt_records = dns.resolver.resolve(domain, 'TXT')
        for record in txt_records:
            record_text = record.to_text()
            emails.update(extract_emails_from_text(record_text))
    except:
        pass
    return list(emails)

def extract_emails_from_page(url):
    """
    Extrai emails de uma página da web.
    """
    emails = set()
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            emails.update(extract_emails_from_text(response.text))
    except:
        pass
    return list(emails)

def extract_emails(domain):
    """
    Realiza a busca completa de emails: na página principal, subdomínios e DNS.
    """
    emails = set()
    
    # Buscar emails no site principal
    emails.update(extract_emails_from_page(f'http://{domain}'))
    emails.update(extract_emails_from_page(f'https://{domain}'))
    
    # Buscar emails nos registros DNS
    emails.update(extract_emails_from_dns(domain))
    
    # Buscar emails em subdomínios conhecidos
    subdomains = ['support', 'contact', 'help', 'mail', 'info', 'dev', 'admin']
    for sub in subdomains:
        sub_url = f'https://{sub}.{domain}'
        emails.update(extract_emails_from_page(sub_url))
    
    return list(emails)

if __name__ == "__main__":
    domain = "google.com"
    found_emails = extract_emails(domain)
    print("Emails encontrados:", found_emails)

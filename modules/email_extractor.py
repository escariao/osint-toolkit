import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def extract_emails_from_text(text):
    """ Extrai emails de um texto, incluindo formatos ofuscados. """
    email_regex = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    alt_email_regex = r'([a-zA-Z0-9_.+-]+)\s*\[at\]\s*([a-zA-Z0-9-]+)\s*\[dot\]\s*([a-zA-Z0-9-.]+)'
    
    emails = set(re.findall(email_regex, text))
    alt_emails = re.findall(alt_email_regex, text)
    
    for alt_email in alt_emails:
        emails.add(f"{alt_email[0]}@{alt_email[1]}.{alt_email[2]}")
    
    return list(emails)

def fetch_html(url):
    """ Obtém o HTML de uma página. """
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None
    return None

def extract_emails(domain):
    """ Coleta emails da página principal e de páginas secundárias """
    base_url = f"http://{domain}"
    emails_found = {}
    
    pages_to_check = ["/", "/contact", "/support", "/help", "/about", "/faq"]
    
    for page in pages_to_check:
        url = urljoin(base_url, page)
        html = fetch_html(url)
        if html:
            emails = extract_emails_from_text(html)
            if emails:
                emails_found[url] = emails
    
    return emails_found

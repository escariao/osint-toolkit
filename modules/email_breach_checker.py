import re
from dorking import google_dork
import requests

def fetch_leaked_emails(domain):
    dork_results = google_dork(f'"@{domain}" site:pastebin.com OR site:github.com OR site:reddit.com')
    leaked_emails = set()

    for url in dork_results:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', response.text)
                leaked_emails.update(emails)
        except requests.exceptions.RequestException:
            continue

    return list(leaked_emails)

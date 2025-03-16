from flask import Flask, render_template, request, redirect, url_for
import whois
import dns.resolver
import requests
from datetime import datetime
from modules.email_extractor import extract_emails
from modules.link_extractor import extract_links
from modules.metadata_extractor import extract_metadata

app = Flask(__name__)

def format_date(date_value):
    """ Formata datas para o formato DD/MM/AAAA """
    if isinstance(date_value, list):
        date_value = date_value[0] if date_value else None
    if isinstance(date_value, datetime):
        return date_value.strftime("%d/%m/%Y")
    return date_value or "N/A"

def get_whois_info(domain):
    try:
        w = whois.whois(domain)
        if not w:
            return {}

        return {
            "Domínio": w.domain_name[0] if isinstance(w.domain_name, list) else w.domain_name,
            "Registradora": w.registrar or "N/A",
            "Servidor WHOIS": w.whois_server or "N/A",
            "Última Atualização": format_date(w.updated_date),
            "Criado em": format_date(w.creation_date),
            "Expira em": format_date(w.expiration_date),
            "Nameservers": ", ".join(w.name_servers) if w.name_servers else "N/A",
            "Status": ", ".join(w.status) if w.status else "N/A",
            "Emails": ", ".join(w.emails) if w.emails else "N/A",
            "Organização": w.org or "N/A",
            "País": w.country or "N/A"
        }
    except:
        return {}

def get_dns_records(domain):
    records = {}
    try:
        records["A"] = [r.address for r in dns.resolver.resolve(domain, 'A')]
    except:
        records["A"] = "Nenhum registro encontrado"

    try:
        records["MX"] = [r.to_text() for r in dns.resolver.resolve(domain, 'MX')]
    except:
        records["MX"] = "Nenhum registro encontrado"

    try:
        records["TXT"] = [r.to_text().strip('"') for r in dns.resolver.resolve(domain, 'TXT')]
    except:
        records["TXT"] = "Nenhum registro encontrado"

    return records

def fetch_html(domain):
    """ Obtém o HTML da página para análise. """
    try:
        response = requests.get(f"http://{domain}", timeout=5)
        if response.status_code == 200:
            return response.text
        return None
    except requests.RequestException:
        return None

def check_social_presence(domain):
    social_media_sites = {
        "Facebook": f"https://www.facebook.com/{domain}",
        "Twitter": f"https://www.twitter.com/{domain}",
        "LinkedIn": f"https://www.linkedin.com/company/{domain}",
        "Instagram": f"https://www.instagram.com/{domain}"
    }
    
    found_profiles = {}
    for platform, url in social_media_sites.items():
        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                found_profiles[platform] = url
        except requests.RequestException:
            pass

    return found_profiles if found_profiles else {}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        domain = request.form["domain"].strip()

        if not domain:
            return render_template("index.html", error="Digite um domínio válido.")

        # Obtendo todas as informações
        whois_data = get_whois_info(domain)  
        dns_records = get_dns_records(domain)
        emails = extract_emails(domain)

        html_content = fetch_html(domain)
        links = extract_links(html_content, f"http://{domain}") if html_content else []

        metadata = extract_metadata(domain)
        metadata = {
            "Título": metadata.get("title", "Não disponível"),
            "Descrição": metadata.get("description", "Não disponível"),
            "Palavras-chave": metadata.get("keywords", "Nenhuma palavra-chave disponível")
        }

        social_profiles = check_social_presence(domain)

        return render_template("result.html",
                               domain=domain,
               

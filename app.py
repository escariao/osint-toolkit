from flask import Flask, render_template, request
import whois
import dns.resolver
import requests
import re
from modules.email_extractor import extract_emails
from modules.link_extractor import extract_links
from modules.metadata_extractor import extract_metadata

app = Flask(__name__)

def get_whois_info(domain):
    try:
        w = whois.whois(domain)
        return w if w else "Nenhuma informação WHOIS disponível."
    except Exception as e:
        return f"Erro ao obter WHOIS: {e}"

def get_dns_records(domain):
    """ Obtém registros DNS do domínio. """
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
        records["TXT"] = [r.to_text() for r in dns.resolver.resolve(domain, 'TXT')]
    except:
        records["TXT"] = "Nenhum registro encontrado"

    return records

def check_social_presence(domain):
    """ Verifica presença do domínio em redes sociais. """
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

    return found_profiles if found_profiles else None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        domain = request.form["domain"]

        # Obtendo os dados
        whois_data = get_whois_info(domain)
        dns_records = get_dns_records(domain)

        # Corrigindo chamadas de funções
        try:
            emails = extract_emails(domain)  # Verifica se o módulo está correto
        except Exception as e:
            emails = f"Erro ao extrair emails: {str(e)}"

        try:
            links = extract_links("<html></html>", domain)  # Agora passa HTML e base_url corretamente
        except Exception as e:
            links = f"Erro ao extrair links: {str(e)}"

        try:
            metadata = extract_metadata(domain)
        except Exception as e:
            metadata = f"Erro ao extrair metadados: {str(e)}"

        social_profiles = check_social_presence(domain)

        return render_template("result.html",
                               domain=domain,
                               whois_data=whois_data,
                               dns_records=dns_records,
                               emails=emails,
                               links=links,
                               metadata=metadata,
                               social_profiles=social_profiles)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

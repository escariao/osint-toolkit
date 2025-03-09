from flask import Flask, render_template, request
import whois
import dns.resolver
import requests
from modules.email_extractor import extract_emails
from modules.link_extractor import extract_links
from modules.metadata_extractor import extract_metadata

app = Flask(__name__)

def get_whois_info(domain):
    try:
        w = whois.whois(domain)
        if not w:
            return "Nenhuma informação WHOIS disponível."
        return str(w) if not isinstance(w, dict) else w
    except Exception as e:
        return f"Erro ao obter WHOIS: {str(e)}"

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
        records["TXT"] = [r.to_text() for r in dns.resolver.resolve(domain, 'TXT')]
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
        domain = request.form["domain"]
        
        whois_data = get_whois_info(domain)
        dns_records = get_dns_records(domain)
        emails = extract_emails(domain)

        html_content = fetch_html(domain)  # Obtendo o HTML antes de chamar extract_links()
        links = extract_links(html_content, f"http://{domain}") if html_content else []

        metadata = extract_metadata(domain)
        social_profiles = check_social_presence(domain)

        return render_template("result.html",
                               domain=domain,
                               whois_data=whois_data or "Nenhuma informação WHOIS disponível",
                               dns_records=dns_records or {},
                               emails=emails or [],
                               links=links or [],
                               metadata=metadata or {},
                               social_profiles=social_profiles or {})

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

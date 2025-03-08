from flask import Flask, render_template, request
import socket
from whois_lookup import get_whois_info
from abuseipdb_lookup import get_abuseipdb_info
from dns_lookup import get_dns_records
from social_lookup import get_social_profiles

app = Flask(__name__)

# Resolver domínio para IP
def resolve_domain(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None

@app.route("/", methods=["GET", "POST"])
def home():
    whois_data, abuseipdb_data, dns_data, social_data = None, None, None, None
    error = None

    if request.method == "POST":
        user_input = request.form["query"].strip()

        if not user_input:
            error = "Nenhum dado foi enviado!"
        else:
            # Se for um domínio, tenta resolver para IP
            if not user_input.replace(".", "").isdigit():
                resolved_ip = resolve_domain(user_input)
                if not resolved_ip:
                    error = f"Domínio '{user_input}' não pôde ser resolvido para um IP válido."
                else:
                    user_input = resolved_ip  # Substitui o domínio pelo IP

            # Se não houver erro, realiza as consultas
            if not error:
                whois_data = get_whois_info(user_input)
                abuseipdb_data = get_abuseipdb_info(user_input)
                dns_data = get_dns_records(user_input)
                social_data = get_social_profiles(user_input)

    return render_template(
        "index.html",
        whois_data=whois_data,
        abuseipdb_data=abuseipdb_data,
        dns_data=dns_data,
        social_data=social_data,
        error=error
    )

if __name__ == "__main__":
    app.run(debug=True)

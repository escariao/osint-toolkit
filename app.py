from flask import Flask, render_template, request, jsonify
import requests
import socket
import whois

app = Flask(__name__)

# CHAVE DA API SHODAN (⚠️ Substitua pela sua chave da Shodan)
SHODAN_API_KEY = "SUA_CHAVE_AQUI"

def resolve_domain(domain):
    """Resolve um domínio para um endereço IP."""
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None

def consultar_whois(dominio):
    """Consulta WHOIS para um domínio."""
    try:
        dados = whois.whois(dominio)
        return {
            "domain_name": dados.domain_name if isinstance(dados.domain_name, str) else dados.domain_name[0],
            "registrar": dados.registrar or "Desconhecido",
            "creation_date": dados.creation_date.strftime('%d/%m/%Y %H:%M:%S') if isinstance(dados.creation_date, str) else dados.creation_date[0].strftime('%d/%m/%Y %H:%M:%S'),
            "expiration_date": dados.expiration_date.strftime('%d/%m/%Y %H:%M:%S') if isinstance(dados.expiration_date, str) else dados.expiration_date[0].strftime('%d/%m/%Y %H:%M:%S'),
        }
    except Exception:
        return {"error": "Não foi possível obter informações WHOIS."}

def consultar_shodan(ip):
    """Consulta a API do Shodan para obter dados do IP."""
    try:
        url = f"https://api.shodan.io/shodan/host/{ip}?key={SHODAN_API_KEY}"
        resposta = requests.get(url)
        dados = resposta.json()
        
        if "error" in dados:
            return {"error": "IP não encontrado no Shodan."}

        return {
            "ip": dados.get("ip_str", "Desconhecido"),
            "org": dados.get("org", "Desconhecido"),
            "os": dados.get("os", "Não identificado"),
            "open_ports": dados.get("ports", []),
            "vulnerabilities": dados.get("vulns", []),
        }
    except Exception as e:
        return {"error": f"Erro na API do Shodan: {str(e)}"}

@app.route("/", methods=["GET", "POST"])
def home():
    data = None
    shodan_data = None
    error = None

    if request.method == "POST":
        user_input = request.form["query"].strip()

        if not user_input:
            error = "Nenhum dado foi enviado!"
        else:
            ip = user_input if user_input.replace(".", "").isdigit() else resolve_domain(user_input)

            if not ip:
                error = f"Domínio '{user_input}' não pode ser resolvido para um IP válido."
            else:
                data = consultar_whois(user_input)
                shodan_data = consultar_shodan(ip)

    return render_template("index.html", data=data, shodan_data=shodan_data, error=error)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request
import whois
import re
import os
import shodan

app = Flask(__name__)

# Obtendo a chave da API do Shodan das variáveis de ambiente
SHODAN_API_KEY = os.getenv("SHODAN_API_KEY")
if not SHODAN_API_KEY:
    print("⚠️ ERRO: A chave da API do Shodan não foi encontrada! Verifique as variáveis de ambiente no Render.")
api = shodan.Shodan(SHODAN_API_KEY)

# Função para buscar informações no Shodan
def get_shodan_info(ip):
    try:
        result = api.host(ip)
        return {
            "ip": result["ip_str"],
            "org": result.get("org", "N/A"),
            "os": result.get("os", "N/A"),
            "vulnerabilities": result.get("vulns", []),
            "open_ports": result.get("ports", [])
        }
    except shodan.APIError as e:
        return {"error": f"Erro na API do Shodan: {e}"}

@app.route("/", methods=["GET", "POST"])
def home():
    data = None
    error = None
    shodan_data = None

    if request.method == "POST":
        query = request.form.get("query")

        # Depuração: Verifica o que o usuário enviou
        print(f"🔍 Entrada do usuário: {query}")

        if not query:
            error = "Nenhum dado foi enviado!"
            return render_template("index.html", error=error)

        # Verifica se é um IP ou Domínio
        if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", query):  # É um IP
            shodan_data = get_shodan_info(query)
            print(f"🛡 Dados do Shodan: {shodan_data}")  # Para depuração

            if "error" in shodan_data:
                error = shodan_data["error"]
        else:  # É um Domínio
            try:
                domain_info = whois.whois(query)
                data = {
                    "domain_name": domain_info.domain_name,
                    "registrar": domain_info.registrar,
                    "creation_date": domain_info.creation_date,
                    "expiration_date": domain_info.expiration_date
                }
            except Exception as e:
                error = f"⚠️ Erro ao buscar WHOIS: {e}"
                print(error)

    return render_template("index.html", data=data, error=error, shodan_data=shodan_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

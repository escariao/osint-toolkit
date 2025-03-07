from flask import Flask, render_template, request, jsonify
import requests
import json
import socket

app = Flask(__name__)

# Substitua com suas chaves de API
SHODAN_API_KEY = "h53uKKpV70ZXZBKtJVwSeM3hSSlVc7XJ"
WHOIS_API_URL = "https://api.whoisxmlapi.com/v1?apiKey=SUA_WHOIS_API_KEY&domain="

# Função para buscar informações no Shodan
def get_shodan_info(ip):
    try:
        url = f"https://api.shodan.io/shodan/host/{ip}?key={SHODAN_API_KEY}"
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return {"error": "Nenhum dado encontrado no Shodan para esse IP."}
        else:
            return {"error": f"Erro do Shodan: {response.status_code}"}
    except Exception as e:
        return {"error": f"Erro ao conectar com a API do Shodan: {str(e)}"}

# Função para buscar informações WHOIS
def get_whois_info(domain):
    try:
        response = requests.get(f"{WHOIS_API_URL}{domain}")
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return {"error": "Nenhum dado WHOIS encontrado para esse domínio."}
        else:
            return {"error": f"Erro na API WHOIS: {response.status_code}"}
    except Exception as e:
        return {"error": f"Erro ao conectar com a API WHOIS: {str(e)}"}

# Resolver domínio para IP
def resolve_domain(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None

@app.route("/", methods=["GET", "POST"])
def home():
    data = None
    error = None
    shodan_data = None
    
    if request.method == "POST":
        user_input = request.form["ip"].strip()
        
        if not user_input:
            error = "Nenhum dado foi enviado!"
        else:
            # Se for um domínio, tenta resolver para IP
            if not user_input.replace(".", "").isdigit():
                resolved_ip = resolve_domain(user_input)
                if not resolved_ip:
                    error = f"Domínio '{user_input}' não pôde ser resolvido para um IP válido. Verifique se ele é acessível."
                else:
                    user_input = resolved_ip
            
            # Se não houver erro, faz as consultas
            if not error:
                data = get_whois_info(user_input)
                shodan_data = get_shodan_info(user_input)
                
                # Verifica erros nas consultas
                if "error" in data:
                    error = data["error"]
                    data = None
                if "error" in shodan_data:
                    error = shodan_data["error"]
                    shodan_data = None
    
    return render_template("index.html", data=data, shodan_data=shodan_data, error=error)

if __name__ == "__main__":
    app.run(debug=True)

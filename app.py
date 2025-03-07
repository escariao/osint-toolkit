from flask import Flask, render_template, request, jsonify
import requests
import json
import socket

app = Flask(__name__)

# Substitua com sua chave de API do AbuseIPDB
ABUSEIPDB_API_KEY = "7652758a92b582f623257d1258cd4512b26ddf7ca4b5d2177bcd9d30578f29fa33fc0737ee25b8a9"
ABUSEIPDB_API_URL = "https://api.abuseipdb.com/api/v2/check"

# Substitua com sua chave de API do Shodan
SHODAN_API_KEY = "h53uKKpV70ZXZBKtJVwSeM3hSSlVc7XJ"

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

# Função para buscar informações no AbuseIPDB
def get_abuseipdb_info(ip):
    headers = {
        "Key": ABUSEIPDB_API_KEY,
        "Accept": "application/json"
    }
    params = {
        "ipAddress": ip,
        "maxAgeInDays": 90
    }
    try:
        response = requests.get(ABUSEIPDB_API_URL, headers=headers, params=params)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return {"error": "Nenhum dado encontrado no AbuseIPDB para esse IP."}
        else:
            return {"error": f"Erro na API AbuseIPDB: {response.status_code}"}
    except Exception as e:
        return {"error": f"Erro ao conectar com a API AbuseIPDB: {str(e)}"}

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
    abuseipdb_data = None
    
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
                abuseipdb_data = get_abuseipdb_info(user_input)
                shodan_data = get_shodan_info(user_input)
                
                # Verifica erros nas consultas
                if "error" in abuseipdb_data:
                    error = abuseipdb_data["error"]
                    abuseipdb_data = None
                if "error" in shodan_data:
                    error = shodan_data["error"]
                    shodan_data = None
    
    return render_template("index.html", abuseipdb_data=abuseipdb_data, shodan_data=shodan_data, error=error)

if __name__ == "__main__":
    app.run(debug=True)

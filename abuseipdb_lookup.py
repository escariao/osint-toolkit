import requests

# Substitua pela sua chave de API do AbuseIPDB
ABUSEIPDB_API_KEY = "957a1c90419b222a37b8b305685cf888edfa6de0c9f2669c74c33955dba22d2d49520b203889d6cc"

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
        response = requests.get("https://api.abuseipdb.com/api/v2/check", headers=headers, params=params)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return {"error": "Nenhum dado encontrado no AbuseIPDB para esse IP."}
        else:
            return {"error": f"Erro na API AbuseIPDB: {response.status_code}"}
    except Exception as e:
        return {"error": f"Erro ao conectar com a API AbuseIPDB: {str(e)}"}

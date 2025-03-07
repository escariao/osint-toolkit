import requests

SHODAN_API_KEY = "h53uKKpV70ZXZBKtJVwSeM3hSSlVc7XJ"

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

import shodan
import os

# Obtém a chave da API a partir das variáveis de ambiente
SHODAN_API_KEY = os.getenv("SHODAN_API_KEY")
api = shodan.Shodan(SHODAN_API_KEY)

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

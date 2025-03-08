import requests

def check_blacklist(domain):
    try:
        response = requests.get(f"https://www.dnsbl.info/dnsbl-database-check.php?query={domain}")
        if response.status_code == 200:
            return "Domínio verificado, consulte o link manualmente."
    except requests.exceptions.RequestException:
        return "Erro ao consultar blacklist."
    
    return "Nenhuma informação encontrada."

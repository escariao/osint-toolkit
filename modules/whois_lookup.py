import whois

def fetch_whois_data(domain):
    try:
        w = whois.whois(domain)
        return {
            "registrar": w.registrar,
            "creation_date": w.creation_date,
            "expiration_date": w.expiration_date,
            "name_servers": w.name_servers,
        }
    except Exception:
        return {"error": "Não foi possível obter informações WHOIS"}

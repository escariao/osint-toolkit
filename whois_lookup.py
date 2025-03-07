import whois

def get_whois_info(domain):
    try:
        w = whois.whois(domain)
        return {
            "domain_name": w.domain_name,
            "registrar": w.registrar or "Desconhecido",
            "creation_date": w.creation_date,
            "expiration_date": w.expiration_date
        }
    except Exception as e:
        return {"error": f"Erro ao consultar WHOIS: {str(e)}"}

import whois

def get_whois_info(domain):
    try:
        w = whois.whois(domain)
        return {
            "domain_name": w.domain_name,
            "registrar": w.registrar if w.registrar else "Desconhecido",
            "creation_date": w.creation_date if w.creation_date else "Desconhecido",
            "expiration_date": w.expiration_date if w.expiration_date else "Desconhecido",
        }
    except Exception as e:
        return {"error": f"Erro ao obter WHOIS: {str(e)}"}

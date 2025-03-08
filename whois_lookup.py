import whois

def get_whois_info(domain):
    try:
        w = whois.whois(domain)

        # Organiza os dados para melhor visualização
        whois_data = {
            "domain_name": w.domain_name,
            "registrar": w.registrar if w.registrar else "Desconhecido",
            "creation_date": w.creation_date if w.creation_date else "Desconhecido",
            "expiration_date": w.expiration_date if w.expiration_date else "Desconhecido",
            "name_servers": w.name_servers if w.name_servers else "Não disponível"
        }
        return whois_data
    except Exception as e:
        return {"error": f"Erro ao buscar WHOIS: {str(e)}"}

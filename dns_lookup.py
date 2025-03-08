import dns.resolver

def get_dns_records(domain):
    try:
        records = {}
        for record_type in ["A", "MX", "NS", "TXT"]:
            try:
                records[record_type] = [r.to_text() for r in dns.resolver.resolve(domain, record_type)]
            except dns.resolver.NoAnswer:
                records[record_type] = "Nenhum registro encontrado."
            except dns.resolver.NXDOMAIN:
                return {"error": "Domínio não encontrado."}
        return records
    except Exception as e:
        return {"error": f"Erro ao buscar registros DNS: {str(e)}"}

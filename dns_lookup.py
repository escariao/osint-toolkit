import dns.resolver

def get_dns_records(domain):
    records = {}
    record_types = ["A", "AAAA", "MX", "NS", "TXT", "CNAME"]

    for record_type in record_types:
        try:
            records[record_type] = [str(r) for r in dns.resolver.resolve(domain, record_type)]
        except dns.resolver.NoAnswer:
            records[record_type] = "Nenhum registro encontrado"
        except dns.resolver.NXDOMAIN:
            return {"error": "Domínio não encontrado"}
        except Exception as e:
            records[record_type] = f"Erro: {str(e)}"

    return records

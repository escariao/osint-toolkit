import dns.resolver

def fetch_dns_records(domain):
    dns_info = {}
    record_types = ["A", "MX", "NS", "TXT"]
    
    for record in record_types:
        try:
            dns_info[record] = [str(r) for r in dns.resolver.resolve(domain, record)]
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.LifetimeTimeout):
            dns_info[record] = ["Nenhuma informação encontrada"]
    
    return dns_info

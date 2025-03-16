from flask import Flask, render_template, request
import whois
import dns.resolver
import requests
from datetime import datetime
from modules.email_extractor import extract_emails
from modules.link_extractor import extract_links
from modules.metadata_extractor import extract_metadata

app = Flask(__name__)

def format_date(date_value):
    """ Formata datas para o formato DD/MM/AAAA """
    if isinstance(date_value, list):
        date_value = date_value[0] if date_value else None
    if isinstance(date_value, datetime):
        return date_value.strftime("%d/%m/%Y")
    return date_value or "N/A"

def get_whois_info(domain):
    try:
        w = whois.whois(domain)
        if not w:
            return "Nenhuma informação WHOIS disponível."

        formatted_whois = {
            "Domínio": w.domain_name if isinstance(w.domain_name, str) else w.domain_name[0] if w.domain_name else "N/A",
            "Registradora": w.registrar or "N/A",
            "Servidor WHOIS": w.whois_server or "N/A",
            "Última Atualização": format_date(w.updated_date),
            "Criado em": format_date(w.creation_date),
            "Expira em": format_date(w.expiration_date),
            "Nameservers": ", ".join(w.name_servers) if w.name_servers else "N/A",
            "Status": ", ".join(w.status) if w.status else "N/A",
            "Emails": ", ".join(w.emails) if w.emails else "N/A",
            "Organização": w.org or "N/A",
            "País": w.country or "N/A"
        }
        return formatted_whois
    except Exception:
        return "Nenhuma informação WHOIS disponível."

def get_dns_records(domain):
    records = {}
    try:
        records["A"] = [r.address for r in dns.resolver.resolve(domain, 'A')]
    except:
        records["A"] = "Nenhum registro encontrado"

    try:
        records["MX"] 

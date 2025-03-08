from flask import Flask, render_template, request
import time
from modules.email_breach_checker import fetch_leaked_emails
from modules.social_scraper import fetch_social_profiles
from modules.dns_lookup import fetch_dns_records
from modules.whois_lookup import fetch_whois_data
from modules.vulnerability_checker import fetch_vulnerabilities
from modules.blacklist_check import check_blacklist

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    target = request.form.get('target')
    if not target:
        return render_template('index.html', error='Por favor, insira um domínio ou IP.')
    
    time.sleep(2)  # Previne sobrecarga nas requisições
    emails = fetch_leaked_emails(target)
    socials = fetch_social_profiles(target)
    dns_records = fetch_dns_records(target)
    whois_info = fetch_whois_data(target)
    vulnerabilities = fetch_vulnerabilities(target)
    blacklist_status = check_blacklist(target)
    
    result_data = {
        'domain': target,
        'emails': emails if emails else ['Nenhum email encontrado'],
        'socials': socials if socials else ['Nenhuma rede social encontrada'],
        'dns_records': dns_records,
        'whois_info': whois_info,
        'vulnerabilities': vulnerabilities if vulnerabilities else ['Nenhuma vulnerabilidade encontrada'],
        'blacklist_status': blacklist_status
    }
    
    return render_template('result.html', result=result_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
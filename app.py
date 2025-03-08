from flask import Flask, render_template, request
import whois
import dns.resolver
import requests
import html

app = Flask(__name__)

def get_whois_info(domain):
    try:
        w = whois.whois(domain)
        return {
            'domain_name': w.domain_name,
            'registrar': w.registrar,
            'creation_date': w.creation_date,
            'expiration_date': w.expiration_date,
            'name_servers': w.name_servers
        }
    except Exception as e:
        return {'error': str(e)}

def get_dns_records(domain):
    records = {}
    try:
        records['A'] = [r.to_text() for r in dns.resolver.resolve(domain, 'A')]
    except:
        records['A'] = []
    try:
        records['MX'] = [r.to_text() for r in dns.resolver.resolve(domain, 'MX')]
    except:
        records['MX'] = []
    try:
        records['TXT'] = [html.unescape(r.to_text()) for r in dns.resolver.resolve(domain, 'TXT')]
    except:
        records['TXT'] = []
    return records

def check_social_presence(username):
    platforms = {
        'Twitter': f'https://twitter.com/{username}',
        'Instagram': f'https://instagram.com/{username}',
        'GitHub': f'https://github.com/{username}'
    }
    found = {}
    for platform, url in platforms.items():
        try:
            response = requests.get(url)
            if response.status_code == 200:
                found[platform] = url
        except:
            pass
    return found if found else None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        domain = request.form.get('domain')
        whois_info = get_whois_info(domain)
        dns_records = get_dns_records(domain)
        social_profiles = check_social_presence(domain.split('.')[0])
        
        return render_template('index.html', whois_info=whois_info, dns_records=dns_records, social_profiles=social_profiles)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

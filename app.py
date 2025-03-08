from flask import Flask, render_template, request
import socket
from whois_lookup import get_whois_info

app = Flask(__name__)

# Resolver domínio para IP
def resolve_domain(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None

@app.route("/", methods=["GET", "POST"])
def home():
    whois_data = None
    error = None

    if request.method == "POST":
        user_input = request.form["query"].strip()

        if not user_input:
            error = "Nenhum dado foi enviado!"
        else:
            if not user_input.replace(".", "").isdigit():
                resolved_ip = resolve_domain(user_input)
                if not resolved_ip:
                    error = f"Domínio '{user_input}' não pôde ser resolvido para um IP válido."
                else:
                    user_input = resolved_ip  

            if not error:
                whois_data = get_whois_info(user_input)

    return render_template("index.html", whois_data=whois_data, error=error)

if __name__ == "__main__":
    app.run(debug=True)

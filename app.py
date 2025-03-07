from flask import Flask, render_template, request
import whois
import re
from shodan_lookup import get_shodan_info

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    data = None
    error = None
    shodan_data = None

    if request.method == "POST":
        query = request.form.get("query")

        # Verifica se é um IP ou Domínio
        if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", query):  # IP
            shodan_data = get_shodan_info(query)
            if "error" in shodan_data:
                error = shodan_data["error"]
        else:  # Domínio
            try:
                domain_info = whois.whois(query)
                data = {
                    "domain_name": domain_info.domain_name,
                    "registrar": domain_info.registrar,
                    "creation_date": domain_info.creation_date,
                    "expiration_date": domain_info.expiration_date
                }
            except Exception as e:
                error = f"Erro ao buscar WHOIS: {e}"

    return render_template("index.html", data=data, error=error, shodan_data=shodan_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

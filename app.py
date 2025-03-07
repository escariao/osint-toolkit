from flask import Flask, render_template, request
import whois

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    data = None
    error = None

    if request.method == "POST":
        domain = request.form.get("domain")

        try:
            domain_info = whois.whois(domain)
            data = {
                "domain_name": domain_info.domain_name,
                "registrar": domain_info.registrar,
                "creation_date": domain_info.creation_date,
                "expiration_date": domain_info.expiration_date
            }
        except Exception as e:
            error = f"Erro ao buscar WHOIS: {e}"

    return render_template("index.html", data=data, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

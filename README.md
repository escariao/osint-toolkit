# 🕵️‍♂️ OSINT TOOLKIT 🔍

![GitHub repo size](https://img.shields.io/github/repo-size/escariao/osint-toolkit)
![GitHub issues](https://img.shields.io/github/issues/escariao/osint-toolkit)
![GitHub license](https://img.shields.io/github/license/escariao/osint-toolkit)
![GitHub last commit](https://img.shields.io/github/last-commit/escariao/osint-toolkit)

O **OSINT Toolkit** é uma ferramenta de **Open Source Intelligence (OSINT)** projetada para **coletar e analisar** informações públicas de forma eficiente. Ele pode extrair **dados WHOIS, DNS, redes sociais, links, metadados** e **e-mails ofuscados**, permitindo investigações digitais mais profundas.

## 🚀 **Principais Funcionalidades**
✔️ **Consulta WHOIS** – Obtém informações de registro de domínios.  
✔️ **Extração de E-mails** – Identifica e-mails explícitos e ofuscados em páginas web.  
✔️ **Análise de Registros DNS** – Obtém registros **A, MX, TXT** e outros.  
✔️ **Coleta de Links** – Identifica links internos e externos em sites.  
✔️ **Verificação de Redes Sociais** – Detecta perfis associados a domínios.  
✔️ **Análise de Metadados** – Extrai **título, descrição e palavras-chave**.  

## 🛠 **Tecnologias Utilizadas**
| Tecnologia | Descrição |
|------------|------------|
| **🐍 Python** | Linguagem principal do projeto |
| **Flask** | Framework web para interface |
| **Requests** | Captura de páginas HTML |
| **BeautifulSoup** | Extração de dados de páginas web |
| **DNSPython** | Consulta de registros DNS |
| **Python-WHOIS** | Análise de domínios WHOIS |
| **Regex** | Extração avançada de e-mails |
| **Render** | Hospedagem do serviço |

## 📌 **Como Usar**

1️⃣ Clone o repositório:
```bash
git clone https://github.com/escariao/osint-toolkit.git
```

2️⃣ Instale as dependências:
```bash
cd osint-toolkit
pip install -r requirements.txt
```

3️⃣ Inicie o servidor:
```bash
python app.py
```

Acesse **http://localhost:5000/** no navegador para utilizar a interface.

## 🌍 **Versão Online**
O OSINT Toolkit também pode ser acessado sem instalação:
[🔗 OSINT Toolkit Online](https://osint-toolkit.onrender.com/)

---
Desenvolvido por **Andrey M. E.** 🕵️‍♂️

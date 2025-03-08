# modules/email_extractor.py

import re

def extract_emails(text):
    """
    Extrai endereços de e-mail de um texto fornecido.

    :param text: Texto contendo possíveis endereços de e-mail.
    :return: Lista de endereços de e-mail encontrados.
    """
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, text)
    return list(set(emails))  # Remove duplicatas

if __name__ == "__main__":
    # Teste rápido
    sample_text = "Entre em contato via email: contato@example.com ou suporte@empresa.com"
    found_emails = extract_emails(sample_text)
    print("E-mails encontrados:", found_emails)

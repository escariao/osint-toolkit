import requests

def get_social_profiles(username):
    social_networks = {
        "Twitter": f"https://twitter.com/{username}",
        "Instagram": f"https://www.instagram.com/{username}",
        "GitHub": f"https://github.com/{username}",
        "LinkedIn": f"https://www.linkedin.com/in/{username}"
    }
    
    found_profiles = {}
    for platform, url in social_networks.items():
        try:
            response = requests.get(url)
            if response.status_code == 200:
                found_profiles[platform] = url
        except Exception as e:
            pass  # Ignora erros de conexão para não interromper a execução
    
    return found_profiles if found_profiles else {"error": "Nenhum perfil encontrado."}

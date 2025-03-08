from modules.dorking import google_dork

def fetch_social_profiles(domain):
    return google_dork(f'"{domain}" site:linkedin.com OR site:twitter.com OR site:facebook.com')

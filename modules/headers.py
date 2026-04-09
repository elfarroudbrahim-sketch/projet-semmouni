#!/usr/bin/env python3

import requests

# --- Couleurs ---
R = '\033[31m'
G = '\033[32m'
C = '\033[36m'
W = '\033[0m'

def get_headers(url):
    """
    Récupère et affiche les headers HTTP(s) d'une URL.
    Retourne un dictionnaire des headers pour usage dans le reste du tool.
    """
    headers_dict = {}
    try:
        # Ajouter https si manquant
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url

        try:
            response = requests.get(url, timeout=5)
        except requests.exceptions.RequestException:
            # fallback HTTP si HTTPS échoue
            url = url.replace("https://", "http://")
            print(f"{C}[!] HTTPS échoué, tentative HTTP...{W}")
            response = requests.get(url, timeout=5)

        print(f"\n{G}[+] Headers trouvés pour {url}:{W}\n")
        for key, value in response.headers.items():
            print(f"{C}{key}{W} : {value}")
            headers_dict[key] = value

    except Exception as e:
        print(f"{R}[-] Erreur lors de la récupération des headers: {e}{W}")

    return headers_dict

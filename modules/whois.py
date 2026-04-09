#!/usr/bin/env python3

import asyncio
import os
from json import load

# --- Couleurs ---
R = '\033[31m'
G = '\033[32m'
C = '\033[36m'
W = '\033[0m'
Y = '\033[33m'

# ================================
# 🔥 Fonction async WHOIS
# ================================
async def get_whois(domain, server):
    """
    Connecte au serveur WHOIS et récupère les informations.
    """
    try:
        reader, writer = await asyncio.open_connection(server, 43)
        writer.write((domain + '\r\n').encode())

        raw_resp = b''
        while True:
            chunk = await reader.read(4096)
            if not chunk:
                break
            raw_resp += chunk

        writer.close()
        await writer.wait_closed()

        return raw_resp.decode(errors="ignore")

    except Exception as e:
        print(f'{R}[-] Erreur connexion WHOIS: {e}{W}')
        return ""

# ================================
# 🔥 Fonction principale
# ================================
def whois_lookup(domain, tld, script_path, output, data):
    """
    Exécute le lookup WHOIS pour un domaine et exporte le résultat si nécessaire.
    """

    # 🔥 IMPORTS ICI (évite circular import)
    from modules.export import export
    from modules.write_log import log_writer

    result = {}

    print(f'\n{Y}[!] Whois Lookup : {W}\n')

    # --- Charger les serveurs WHOIS ---
    db_path = os.path.join(script_path, 'modules', 'whois_servers.json')

    try:
        with open(db_path, 'r') as f:
            db_json = load(f)
    except FileNotFoundError:
        print(f'{R}[-] Fichier whois_servers.json introuvable: {db_path}{W}')
        return
    except Exception as e:
        print(f'{R}[-] Erreur lecture whois_servers.json: {e}{W}')
        return

    # --- Vérification du TLD ---
    whois_server = db_json.get(tld)
    if not whois_server:
        print(f'{R}[-] TLD non supporté: {tld}{W}')
        return

    # --- Exécution WHOIS ---
    full_domain = f"{domain}.{tld}"
    try:
        raw_data = asyncio.run(get_whois(full_domain, whois_server))
        if not raw_data:
            print(f'{R}[-] Aucun résultat pour {full_domain}{W}')
            return

        print(raw_data)
        result['whois'] = raw_data

    except Exception as e:
        print(f'{R}[-] Erreur WHOIS: {e}{W}')
        log_writer(f'[whois] Exception = {e}')
        return

    # --- Export ---
    if output:
        try:
            os.makedirs(output["directory"], exist_ok=True)
            fname = os.path.join(output["directory"], f'whois.{output["format"]}')
            output['file'] = fname
            data['module-whois'] = result
            export(output, data)
            result['exported'] = True
            print(f'{G}[+] WHOIS exporté vers: {fname}{W}')
        except Exception as e:
            print(f'{R}[-] Erreur export WHOIS: {e}{W}')
            result['exported'] = False

    log_writer('[whois] Completed')

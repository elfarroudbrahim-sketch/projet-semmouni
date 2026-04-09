#!/usr/bin/env python3

import os
import sys
import argparse
import tldextract
import importlib
import re
import socket

# --- Couleurs ---
R = '\033[31m'
G = '\033[32m'
C = '\033[36m'
Y = '\033[33m'
W = '\033[0m'

# --- Path ---
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, BASE_DIR)

# --- Imports modules ---
try:
    extract_pdf_meta = importlib.import_module("modules.metadata").extract_pdf_meta
    find_emails = importlib.import_module("modules.search_emails").find_emails
    log_writer = importlib.import_module("modules.write_log").log_writer
except Exception as e:
    print(f"[ERROR] Module import failed: {e}")
    sys.exit(1)

import settings as config

# --- Version ---
VERSION = '1.4.1'
log_writer(f'FinalRecon v{VERSION}')

# ================================
# 🔥 Arguments
# ================================
parser = argparse.ArgumentParser(description=f'FinalRecon - All in One Web Recon | v{VERSION}')

parser.add_argument('--url', help='Target URL')
parser.add_argument('--headers', action='store_true', help='Header Information')
parser.add_argument('--ps', action='store_true', help='Fast Port Scan')
parser.add_argument('--whois', action='store_true', help='Whois Lookup')
parser.add_argument('--dns', action='store_true', help='DNS Enumeration')
parser.add_argument('--emails', action='store_true', help='Email search')
parser.add_argument('--meta', type=str, help='Extract PDF metadata')
parser.add_argument('--hibp', type=str, help="Check email leaks (HIBP)")
parser.add_argument('--full', action='store_true', help='Full Recon')

parser.add_argument('-d', default="1.1.1.1", help='DNS Server')
parser.add_argument('-o', default="txt", help='Export format')
parser.add_argument('-cd', default="./output", help='Output directory')

args = parser.parse_args()

# ================================
# 🔥 Variables
# ================================
target = args.url
dns_flag = args.dns
whois_flag = args.whois
emails_flag = args.emails
hibp_target = args.hibp
full = args.full

dserv = args.d
output = args.o
output_dir = args.cd

# ================================
# 🔥 Utils
# ================================
def is_ip(value):
    return re.match(r"^\d+\.\d+\.\d+\.\d+$", value)

# ================================
# 🔥 Check URL
# ================================
if not target and not hibp_target:
    print(f'{R}[!] URL ou email requis (--url ou --hibp){W}')
    sys.exit(1)

if target:
    domain = target.replace('http://', '').replace('https://', '').split('/')[0]

    # 🔥 Résolution IP
    try:
        ip = socket.gethostbyname(domain)
        print(f"{G}[+] IP cible: {C}{ip}{W}")
    except:
        print(f"{R}[-] Résolution DNS échouée{W}")

    # 🔥 Détection IP
    if is_ip(domain):
        print(f"{Y}[INFO] Mode IP → DNS & WHOIS ignorés{W}")

data = {}

# ================================
# 🔥 1. DNS
# ================================
if target and (dns_flag or full) and not is_ip(domain):
    print(f'\n{G}[+] DNS pour: {C}{domain}{W}')
    try:
        dns_module = importlib.import_module("modules.dns")
        dns_module.dnsrec(
            domain,
            dserv,
            {"directory": output_dir, "format": output},
            data
        )
    except Exception as e:
        print(f'{R}[-][DNS] {e}{W}')

# ================================
# 🔥 2. WHOIS
# ================================
if target and (whois_flag or full) and not is_ip(domain):
    print(f'\n{G}[+] WHOIS pour: {C}{domain}{W}')
    try:
        whois_module = importlib.import_module("modules.whois")

        ext = tldextract.extract(domain)
        tld = ext.suffix
        domain_name = ext.domain

        if not tld:
            print(f"{Y}[INFO] Domaine invalide pour WHOIS{W}")
        else:
            whois_module.whois_lookup(
                domain_name,
                tld,
                BASE_DIR,
                {"directory": output_dir, "format": output},
                data
            )

    except Exception as e:
        print(f'{R}[-][WHOIS] {e}{W}')

# ================================
# 🔥 3. EMAILS
# ================================
if target and (emails_flag or full):
    print(f'\n{G}[+] Emails pour: {C}{domain}{W}')
    try:
        email_target = target
        if not email_target.startswith("http://") and not email_target.startswith("https://"):
            email_target = "http://" + email_target

        find_emails(email_target)
    except Exception as e:
        print(f'{R}[-][Emails] {e}{W}')

# ================================
# 🔥 4. METADATA
# ================================
if args.meta:
    print(f'\n{G}[+] Metadata: {C}{args.meta}{W}')
    try:
        extract_pdf_meta(args.meta)
    except Exception as e:
        print(f'{R}[-][Metadata] {e}{W}')

# ================================
# 🌐 5. HEADERS + ANALYSE
# ================================
if target and (args.headers or full):
    print(f'\n{G}[+] Headers pour: {C}{target}{W}')
    try:
        headers_module = importlib.import_module("modules.headers")
        headers = headers_module.get_headers(target)

        # 🔥 Analyse vulnérabilités basique
        if headers:
            server = headers.get("Server", "")
            php = headers.get("X-Powered-By", "")

            print(f"\n{C}[Analyse Sécurité]{W}")

            if "Apache/2.2" in server:
                print(f"{Y}[!] Apache obsolète détecté{W}")

            if "PHP/5.2" in php:
                print(f"{Y}[!] PHP vulnérable détecté{W}")

    except Exception as e:
        print(f'{R}[-][HEADERS] {e}{W}')

# ================================
# 🔍 6. PORT SCAN
# ================================
if target and (args.ps or full):
    print(f'\n{G}[+] Scan des ports pour: {C}{domain}{W}')
    try:
        portscan_module = importlib.import_module("modules.portscan")
        portscan_module.port_scan(domain)
    except Exception as e:
        print(f'{R}[-][PORTSCAN] {e}{W}')

# ================================
# 💣 7. HIBP
# ================================
if hibp_target:
    print(f'\n{G}[+] HIBP pour: {C}{hibp_target}{W}')
    try:
        hibp_module = importlib.import_module("modules.hibp")
        hibp_module.check_breach(hibp_target)
    except Exception as e:
        print(f'{R}[-][HIBP] {e}{W}')

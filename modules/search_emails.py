import requests
import re

def find_emails(url):
    print(f'\n[+] Searching for Emails on: {url}')
    try:
        header = {'User-Agent': 'Mozilla/5.0'}
        req = requests.get(url, headers=header, timeout=10)
        # Regex pour trouver des adresses emails
        emails = re.findall(r'[a-zA-Z0-9.\-_]+@[a-zA-Z0-9.\-_]+\.[a-z]{2,4}', req.text)
        
        if emails:
            for email in set(emails): # set() pour éviter les doublons
                print(f'  |-- Email found: {email}')
        else:
            print('  [-] No emails found on the main page.')
    except Exception as e:
        print(f'  [!] Error: {e}')

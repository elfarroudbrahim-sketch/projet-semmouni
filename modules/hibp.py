import requests

R = '\033[31m'
G = '\033[32m'
C = '\033[36m'
W = '\033[0m'
Y = '\033[33m'

def check_breach(email):

    print(f"\n{Y}[!] Checking breaches for: {C}{email}{W}\n")

    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"

    headers = {
        "User-Agent": "FinalRecon"
    }

    try:
        r = requests.get(url, headers=headers)

        if r.status_code == 200:
            for b in r.json():
                print(f"{R}[BREACH]{W} {b['Name']} - {b['BreachDate']}")
        elif r.status_code == 404:
            print(f"{G}[+] No breach found{W}")
        else:
            print(f"{R}[-] API Error: {r.status_code}{W}")

    except Exception as e:
        print(f"{R}[-] Error: {e}{W}")

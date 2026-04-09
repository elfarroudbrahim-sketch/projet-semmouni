#!/usr/bin/env python3

import socket

R = '\033[31m'
G = '\033[32m'
C = '\033[36m'
W = '\033[0m'


def port_scan(target):
    ports = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 8080]

    print(f"{G}[+] Scan ports en cours...{W}\n")

    for port in ports:
        try:
            sock = socket.socket()
            sock.settimeout(0.5)

            result = sock.connect_ex((target, port))

            if result == 0:
                print(f"{C}Port {port}{W} : {G}OPEN{W}")

            sock.close()

        except Exception:
            pass

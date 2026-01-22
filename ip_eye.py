#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ip eye - IP Tracking Tool by n0merc
# GitHub: https://github.com/n0merc/ip-eye

import os
import sys
import socket
import json
import requests
import threading
from datetime import datetime
from colorama import init, Fore, Style
import dns.resolver
import whois
import shodan

init(autoreset=True)

BANNER = f"""{Fore.RED}
██╗██████╗     ███████╗██╗   ██╗███████╗
██║██╔══██╗    ██╔════╝╚██╗ ██╔╝██╔════╝
██║██████╔╝    █████╗   ╚████╔╝ █████╗  
██║██╔═══╝     ██╔══╝    ╚██╔╝  ██╔══╝  
██║██║         ███████╗   ██║   ███████╗
╚═╝╚═╝         ╚══════╝   ╚═╝   ╚══════╝
{Style.RESET_ALL}
{Fore.RED}ip eye - IP Tracking Tool{Style.RESET_ALL}
{Fore.YELLOW}Made by n0merc{Style.RESET_ALL}
"""

CONFIG_FILE = "config.json"

class IPEye:
    def __init__(self):
        self.api_keys = self.load_keys()

    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    def banner(self):
        self.clear()
        print(BANNER)

    def load_keys(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        return {"shodan": ""}

    def save_keys(self):
        with open(CONFIG_FILE, "w") as f:
            json.dump(self.api_keys, f, indent=4)

    def ip_info(self, ip):
        print(f"{Fore.YELLOW}[*] Tracking IP: {ip}")
        try:
            socket.inet_aton(ip)
        except:
            print(f"{Fore.RED}[!] Invalid IP")
            return None

        r = requests.get(f"https://ipinfo.io/{ip}/json", timeout=10)
        if r.status_code != 200:
            return None

        data = r.json()
        for k, v in data.items():
            print(f"{Fore.CYAN}{k:<12}{Fore.WHITE}: {v}")

        if "loc" in data:
            print(f"\n{Fore.GREEN}MAP:")
            print(f"https://maps.google.com/?q={data['loc']}")

        return data

    def port_scan(self, ip, start=1, end=100):
        print(f"{Fore.YELLOW}[*] Port scan {start}-{end}")
        open_ports = []

        def scan(p):
            try:
                s = socket.socket()
                s.settimeout(1)
                if s.connect_ex((ip, p)) == 0:
                    print(f"{Fore.GREEN}[+] Open port {p}")
                    open_ports.append(p)
                s.close()
            except:
                pass

        threads = []
        for p in range(start, end + 1):
            t = threading.Thread(target=scan, args=(p,))
            threads.append(t)
            t.start()
            if len(threads) >= 100:
                for th in threads:
                    th.join()
                threads = []

        for th in threads:
            th.join()

        return open_ports

    def dns_lookup(self, domain):
        print(f"{Fore.YELLOW}[*] DNS lookup {domain}")
        for rtype in ["A", "AAAA", "MX", "NS", "TXT", "CNAME"]:
            try:
                answers = dns.resolver.resolve(domain, rtype)
                print(f"{Fore.CYAN}{rtype} records:")
                for r in answers:
                    print(f"  {r}")
            except:
                pass

    def reverse_dns(self, ip):
        try:
            host = socket.gethostbyaddr(ip)
            print(f"{Fore.GREEN}[+] Hostname: {host[0]}")
            return host[0]
        except:
            print(f"{Fore.RED}[-] No reverse record")
            return None

    def whois_lookup(self, target):
        try:
            w = whois.whois(target)
            print(w)
        except Exception as e:
            print(f"{Fore.RED}[-] WHOIS failed: {e}")

    def shodan_search(self, query):
        if not self.api_keys.get("shodan"):
            print(f"{Fore.RED}[!] Shodan key not set")
            return
        try:
            api = shodan.Shodan(self.api_keys["shodan"])
            res = api.search(query)
            print(f"{Fore.GREEN}[+] Results: {res['total']}")
            for m in res["matches"][:10]:
                print(f"\nIP: {m['ip_str']}  PORT: {m['port']}")
                print(m.get("data", "")[:300])
        except Exception as e:
            print(f"{Fore.RED}[-] Shodan error: {e}")

    def report(self, ip, data, ports):
        name = f"ip_eye_report_{ip}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(name, "w") as f:
            f.write("IP EYE REPORT\n")
            f.write(f"TARGET: {ip}\n\n")
            for k, v in data.items():
                f.write(f"{k}: {v}\n")
            if ports:
                f.write("\nOPEN PORTS:\n")
                for p in ports:
                    f.write(str(p) + "\n")
        print(f"{Fore.GREEN}[+] Saved {name}")

    def menu(self):
        print(f"""
{Fore.GREEN}1{Fore.WHITE} Track IP
{Fore.GREEN}2{Fore.WHITE} Port Scan
{Fore.GREEN}3{Fore.WHITE} DNS Lookup
{Fore.GREEN}4{Fore.WHITE} Reverse DNS
{Fore.GREEN}5{Fore.WHITE} WHOIS
{Fore.GREEN}6{Fore.WHITE} Shodan
{Fore.GREEN}7{Fore.WHITE} Set API Key
{Fore.GREEN}0{Fore.WHITE} Exit
""")

    def run(self):
        while True:
            self.banner()
            self.menu()
            c = input("ip-eye > ")

            if c == "1":
                ip = input("IP: ")
                self.ip_info(ip)
                input()
            elif c == "2":
                ip = input("IP: ")
                self.port_scan(ip)
                input()
            elif c == "3":
                d = input("Domain: ")
                self.dns_lookup(d)
                input()
            elif c == "4":
                ip = input("IP: ")
                self.reverse_dns(ip)
                input()
            elif c == "5":
                t = input("Target: ")
                self.whois_lookup(t)
                input()
            elif c == "6":
                q = input("Query: ")
                self.shodan_search(q)
                input()
            elif c == "7":
                k = input("Shodan API key: ")
                self.api_keys["shodan"] = k
                self.save_keys()
            elif c == "0":
                sys.exit()
            else:
                pass

def main():
    IPEye().run()

if __name__ == "__main__":
    main()


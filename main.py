import os
import re
import base64
import requests
from datetime import datetime
from colorama import Fore, Style, init
import time


class DiscordPromoChecker:
    def __init__(self, country_code="IN"):
        init(autoreset=True)
        self.cleamterminal()
        self.ascii()
        self.session = requests.Session()
        self.country_code = country_code
        self.promo_codes = self.getpromos()

        self.color_codes = {
            "yellow": "\033[38;2;252;240;3m",
            "green": "\033[38;2;3;252;32m",
            "pink": "\033[38;2;255;36;226m",
            "blue": "\033[38;2;89;114;255m",
            "red": "\033[38;2;255;31;31m",
            "purple": "\033[38;2;141;10;255m"
        }
        
        self.params = {
            "country_code": self.country_code,
            "with_application": "false",
            "with_subscription_plan": "true"
        }

        self.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6,bn;q=0.5",
            "Authorization": "MTM3MzMxNTU3MzIzNjEwNTI2Ng.Gis7dE.y_kTfRcnwYnBvZ1H-WbVBYWC92MlUdYFlJMiGY",
            "Cookie": "__dcfduid=e69cf0209c5611ef99ee6bc502972094; __sdcfduid=e69cf0219c5611ef99ee6bc502972094aea0b69cad49b5549f1a1672d612021d149c6e5d62543c5c190859f07ca1a7e6; __stripe_mid=cb39e45e-dc43-4e50-923d-904abd72dd09a9a152; dbind=a60ace96-73f4-452f-adf4-e82cae2bf615; _gcl_au=1.1.2071494670.1744036442; _ga_YL03HBJY7E=GS1.1.1744113556.2.0.1744113556.0.0.0; _ga=GA1.1.916087961.1730910621; OptanonConsent=isIABGlobal=false&datestamp=Mon+May+05+2025+13%3A21%3A11+GMT%2B0530+(India+Standard+Time)&version=202501.2.0&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false&isGpcEnabled=0&browserGpcFlag=0; _ga_Q149DFWHT7=GS2.1.s1746431471$o4$g0$t1746431471$j0$l0$h0; _ga_5CWMJQ1S0X=GS2.1.s1746431428$o1$g1$t1746431800$j0$l0$h0; perf_dv6Tr4b=1; __stripe_sid=8200c8a6-9b3e-46cf-a439-39c9e10312ac62fb90; cf_clearance=La.edWvVIa3a_8IhEHbRC68G0MxVj5ruJLOnOr_1NO0-1747463460-1.2.1.1-W2jlVytE_3oWx74HEAOKycwzesPjPB6N8JFbaHrJEoGlgFpnEGPevcROVKKf1WOmdR9RhG0zPMioWCy2X49DiQDA_jWWZ1jhdNy74eaP6_Yt6sb4UqqsTc7zLu28oFD4kcvxjolw6UHYOPV_DFrBCUi4e6CkK2bJYiQTt6KHCFu7E4t8oMUxSyGqi1kgLArfSfNkedLjRJIG8mKoqdR0VKSk48AuArRG.kdevWvhX0kKGlPR5HSYpNn6.U1fYeqEZXjanAmHfk1NGK5TlaZiyFGQZXlP.iLm.YOz0jdPld7g7G1SLHWaKgrAu5XOhlVz_fYmfnRlzUXSeToz6E.v9G1EjJDb8rmliSvGzdG5dv4; __cfruid=1822f55402a63dde583a2fcbeaa17ea306cdd02a-1747463461; _cfuvid=frCuVSwL8v9Tg6X0R9It56ZarKAuBKwe9dliHZOjW_g-1747463461553-0.0.1.1-604800000",
            "Priority": "u=1, i",
            "Sec-Ch-Ua": '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
            "Sec-Ch-Ua-Mobile": "?1",
            "Sec-Ch-Ua-Platform": '"Android"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Mobile Safari/537.36",
            "X-Debug-Options": "bugReporterEnabled",
            "X-Discord-Locale": "en-US",
            "X-Discord-Timezone": "Asia/Calcutta",
            "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLUlOIiwiaGFzX2NsaWVudF9tb2RzIjpmYWxzZSwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKExpbnV4OyBBbmRyb2lkIDYuMDsgTmV4dXMgNSBCdWlsZC9NUkE1OE4pIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8xMzYuMC4wLjAgTW9iaWxlIFNhZmFyaS81MzcuMzYiLCJicm93c2VyX3ZlcnNpb24iOiIxMzYuMC4wLjAiLCJvc192ZXJzaW9uIjoiNi4wIiwicmVmZXJyZXIiOiJodHRwczovL2Rpc2NvcmQuY29tLz9kaXNjb3JkdG9rZW49TVRNMk9Ua3hNall4TkRZNU9Ua3lOVFUzTmcuR21KVmlFLjFvZjNDRmxRcEhzM05IS3k5b01yc0lnNHR4V0lFQ2F4d2gtXzRRIiwicmVmZXJyaW5nX2RvbWFpbiI6ImRpc2NvcmQuY29tIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjQwMDQ1MywiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbCwiY2xpZW50X2xhdW5jaF9pZCI6IjA4NWUzOWIxLTNiZGItNDY0MS1iNTljLTA5ZDJmNDEyMTFjZiIsImNsaWVudF9oZWFydGJlYXRfc2Vzc2lvbl9pZCI6ImQ5MDk1ODMxLTUyMDAtNDkxMS05ODE0LTQ0OTU2OTM0ODEyZSJ9"
        }

    def ascii(self):
        ascii_art = """
 █████                                                   
░░███                                                    
 ░███   ██████   ██████  ████████   ████████   ████████  
 ░███  ███░░███ ███░░███░░███░░███ ░░███░░███ ░░███░░███ 
 ░███ ░███ ░░░ ░███ ░███ ░███ ░███  ░███ ░███  ░███ ░███ 
 ░███ ░███  ███░███ ░███ ░███ ░███  ░███ ░███  ░███ ░███ 
 █████░░██████ ░░██████  ████ █████ ████ █████ ████ █████
░░░░░  ░░░░░░   ░░░░░░  ░░░░ ░░░░░ ░░░░ ░░░░░ ░░░░ ░░░░░ 
                                                         
"""                                  
        pc = "\033[38;2;141;10;255m"
        e = "aHR0cHM6Ly9naXRodWIuY29tL2ljb254eXp6"
        d = base64.b64decode(e).decode("utf-8")
        w = os.get_terminal_size().columns
        print(pc + "\n".join(line.center(w) for line in ascii_art.splitlines()))
        print(Style.RESET_ALL + "\n")

    def cleamterminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def getpromos(self):
        try:
            with open('input.txt') as f:
                return re.findall(r'/promotions/(\w+)', f.read()) or []
        except FileNotFoundError:
            print(f"{Fore.RED}[-] Error: input.txt file not found")
            exit()

    def formattedpromo(self, code):
        return code if len(code) <= 8 else f"{code[:8]}............{code[-8:]}"

    def save(self, filename, promo_code):
        try:
            with open(filename, 'a') as f:
                f.write(f"https://discord.com/billing/promotions/{promo_code}\n")
        except IOError as e:
            print(f"{Fore.RED}Error saving to {filename}: {e}")

    def check(self, promo_code):
        formatted_promo = self.formattedpromo(promo_code)
        current_time = datetime.now().strftime("%H:%M:%S")
        self.headers["Referer"] = f"https://discord.com/billing/promotions/{promo_code}"
        
        try:
            response = self.session.get(
                f"https://discord.com/api/v9/entitlements/gift-codes/{promo_code}", headers=self.headers, params=self.params)
            
            if response.status_code == 401:
                print(f"{Fore.WHITE} >> Promo - {self.color_codes['red']}{formatted_promo} >> Invalid Token")
                return
            
            if response.status_code == 429:
                print(f"{Fore.WHITE} >> Promo - {self.color_codes['red']}{formatted_promo} >> Rate Limited")
                time.sleep(5)
                return
            
            if response.status_code == 404:
                print(f"{Fore.WHITE} >> Promo - {self.color_codes['red']}{formatted_promo} >> Invalid")
                self.save('invalid.txt', promo_code)
            
            elif response.status_code == 200:
                data = response.json()
                uses = data.get('uses', 0)
                
                if uses == 1:
                    print(f"{Fore.WHITE} >> Promo - {self.color_codes['red']}{formatted_promo} | Redeemed")
                    self.save('redeemed.txt', promo_code)
                else:
                    trial = data.get('subscription_trial', {})
                    interval = trial.get('interval_count', 1)

                    duration_map = {
                        1: ("1m", '1mvalid.txt'),
                        3: ("3m", '3mvalid.txt')
                    }
                    duration, filename = duration_map.get(interval, (f"{interval}m", 'valid.txt'))

                    days_remaining = 0
                    expiry_date = data.get('expires_at')
                    if expiry_date:
                        end_date = datetime.fromisoformat(expiry_date.replace('Z', '+00:00'))
                        days_remaining = (end_date - datetime.now(end_date.tzinfo)).days

                    print(
                        f"{Fore.WHITE} >> Promo - {self.color_codes['green']}{formatted_promo} | {self.color_codes['yellow']}Duration: {duration} | {self.color_codes['pink']}Redeemed: False | {self.color_codes['blue']}Expires In: {days_remaining}d")
                    self.save(filename, promo_code)
            
            else:
                print(f"{Fore.WHITE} >> Unknown Status: {response.status_code}")
                
        except Exception as e:
            print(f"{Fore.WHITE}[{current_time}] >> Error: {str(e)}")

    def run(self):
        if not self.promo_codes:
            print(f"{Fore.RED}(-) No promo codes found in input.txt")
            return

        for promo_code in self.promo_codes:
            self.check(promo_code)

        print(f"\n\n{Fore.WHITE}(+) Finished checking promo codes !!")
        input(f"\n{Fore.YELLOW}(#) Press Enter to exit")
        
if __name__ == "__main__":
    checker = DiscordPromoChecker()
    checker.run()

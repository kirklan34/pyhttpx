import sys

import httpx
import io
import argparse
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init

init(autoreset=True)

SECURITY_HEADERS = [
    "Content-Security-Policy",
    "Strict-Transport-Security",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
    "Permissions-Policy"
]

def print_banner():
    banner = f"""
{Fore.CYAN}{Style.BRIGHT}
██████╗ ██╗   ██╗██╗  ██╗████████╗████████╗██████╗ ██╗  ██╗██╗  ██╗
██╔══██╗██║   ██║██║ ██╔╝╚══██╔══╝╚══██╔══╝██╔══██╗██║ ██╔╝╚██╗██╔╝
██████╔╝██║   ██║█████╔╝    ██║      ██║   ██████╔╝█████╔╝  ╚███╔╝ 
██╔═══╝ ██║   ██║██╔═██╗    ██║      ██║   ██╔═══╝ ██╔═██╗  ██╔██╗ 
██║     ╚██████╔╝██║  ██╗   ██║      ██║   ██║     ██║  ██╗██╔╝ ██╗
╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝
        {Fore.MAGENTA}      HTTP Security & Technology Scanner
            {Fore.RED}  This tool is intended solely for use in controlled environments and only with proper authorization.
        """
    print(banner)


def detect_technology(url, response):
    tech = []
    html = response.text.lower()
    cookies = response.headers.get("Set-Cookie", "").lower()
    powered_by = response.headers.get("X-Powered-By", "").lower()

    server = response.headers.get("Server", "")
    if server:
        tech.append(f"Server: {server}")
    if powered_by:
        tech.append(f"X-Powered-By: {powered_by}")

    if "wordpress" in cookies or "wp-settings" in cookies:
        tech.append("WordPress (cookie)")
    if "wp-content" in html or "wp-includes" in html:
        tech.append("WordPress (HTML content)")
    try:
        wp = httpx.get(url.rstrip("/") + "/wp-login.php", timeout=5)
        if "wordpress" in wp.text.lower():
            tech.append("WordPress (wp-login.php)")
    except:
        pass

    if "phpsessid" in cookies or "php" in powered_by:
        tech.append("PHP")

    if "laravel_session" in cookies:
        tech.append("Laravel")

    if "csrftoken" in cookies:
        tech.append("Django")
    if "sessionid" in cookies and "django" in html:
        tech.append("Django (HTML ref)")

    if "express" in powered_by:
        tech.append("Node.js (Express)")

    if "joomla" in html or "joomla" in cookies:
        tech.append("Joomla")

    if "drupal" in html or "/sites/all" in html:
        tech.append("Drupal")

    if tech:
        print(f"{Fore.BLUE}[TECH] Detected: {', '.join(set(tech))}")

def check_url(url):
    try:
        response = httpx.get(url, timeout=5)
        status_color = Fore.GREEN if response.status_code < 400 else Fore.RED
        print(f"\n{Style.BRIGHT}{Fore.YELLOW}==> URL: {url}")
        print(f"{status_color}[{response.status_code}] {url}")

        missing_headers = [h for h in SECURITY_HEADERS if h not in response.headers]
        if missing_headers:
            for header in missing_headers:
                print(f"{Fore.RED}[WARNING] Missing security header: {header}")
        else:
            print(f"{Fore.GREEN}[OK] All key security headers present.")

        detect_technology(url, response)

    except httpx.RequestError as e:
        print(f"{Fore.RED}[ERROR] {url} - {type(e).__name__}")
    except Exception as e:
        print(f"{Fore.RED}[ERROR] {url} - {type(e).__name__}")

def run_checks(urls):
    with ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(check_url, urls)

def main():
    print_banner()
    parser = argparse.ArgumentParser(description="pyhttpx - HTTP status checker")
    parser.add_argument("-l", "--list", help="File with URLs", required=True)
    parser.add_argument("--report", "-r", action='store_true', help="Make a report")
    args = parser.parse_args()

    try:
        with open(args.list, "r") as file:
            urls = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"{Fore.RED}[!] File not found: {args.list}")
        return

    if args.report:
        # Capturar salida en buffer y guardar en archivo
        buffer = io.StringIO()
        sys_stdout_original = sys.stdout
        sys.stdout = buffer
        try:
            run_checks(urls)
        finally:
            sys.stdout = sys_stdout_original

        salida = buffer.getvalue()
        print(salida)  # Opcional: muestra la salida también por consola

        with open("report.txt", "w") as f:
            f.write(salida)
    else:
        run_checks(urls)

if __name__ == "__main__":
    main()

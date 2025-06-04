import httpx
import argparse
from concurrent.futures import ThreadPoolExecutor

def check_url(url):
    try:
        response = httpx.get(url, timeout=5)
        print(f"[{response.status_code}] {url}")
    except httpx.RequestError as e:
        print(f"[ERROR] {url} - {type(e).__name__}")
    except Exception as e:
        print(f"[ERROR] {url} - {type(e).__name__}")

def main():
    parser = argparse.ArgumentParser(description="pyhttpx - HTTP status checker")
    parser.add_argument("-l", "--list", help="File with URLs", required=True)
    args = parser.parse_args()

    try:
        with open(args.list, "r") as file:
            urls = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"[!] File not found: {args.list}")
        return

    with ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(check_url, urls)

if __name__ == "__main__":
    main()

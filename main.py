import sys, requests

def main():
    args = sys.argv

    if len(args) < 2:
        print("no website provided") 
        sys.exit(1)
    elif len(args) > 2:
        print("too many arguments provided")
        sys.exit(1)
    else:
        print(f"starting crawl of: {args[1]}")
        url = args[1]

    print(get_html(url))

def get_html(url: str) -> str:
    response = requests.get(url, headers={"User-Agent": "BootCrawler/1.0"})

    if response.status_code >= 400:
        raise Exception("Request failed")
    if 'text/html' not in response.headers['Content-Type']:
        raise Exception(f'Incorrect content type: {response.headers["Content-Type"]}')
    if response.status_code != 200:
        raise Exception(f'Error: {response.status_code} - {response.raise_for_status}')
    return response.text

if __name__ == "__main__":
    main()

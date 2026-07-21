from urllib.parse import urlsplit

def normalize_url(url: str) -> str:
    parts = urlsplit(url)
    domain = parts.netloc
    path = parts.path

    if path.endswith("/"):
        path = parts.path[:-1]
    
    return f'{domain}{path}'
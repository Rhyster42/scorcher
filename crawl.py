from urllib.parse import urlsplit
from bs4 import BeautifulSoup, Tag

def normalize_url(url: str) -> str:
    parts = urlsplit(url)
    domain = parts.netloc
    path = parts.path

    if path.endswith("/"):
        path = parts.path[:-1]
    
    return f'{domain}{path}'

def get_heading_from_html(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')

    h_tag = soup.h1
    if isinstance(h_tag, Tag)==False:
        h_tag = soup.h2
    
    return h_tag.get_text(strip=True, separator=" ") if isinstance(h_tag, Tag) else ""

def get_first_paragraph_from_html(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')

    p_tag = soup.p
    if isinstance(soup.main, Tag):
        p_tag = soup.main.p

    return p_tag.get_text(strip=True, separator=" ") if isinstance(p_tag, Tag) else ""
from urllib.parse import urlsplit, urljoin
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

    h_tag = soup.find("h1") or soup.find("h2")
    
    return h_tag.get_text(strip=True, separator=" ") if isinstance(h_tag, Tag) else ""

def get_first_paragraph_from_html(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')

    p_tag = soup.p
    if isinstance(soup.main, Tag):
        p_tag = soup.main.p

    return p_tag.get_text(strip=True, separator=" ") if isinstance(p_tag, Tag) else ""

def get_urls_from_html(html: str, base_url: str):
    soup = BeautifulSoup(html, 'html.parser')
    abs_path_list = []

    anchors = soup.find_all('a')

    for item in anchors:
        if not isinstance(item, Tag):
            continue
        href = item.get('href') 
        if isinstance(href, str) and href:
            try:
                abs_path_list.append(urljoin(base_url, href))
            except Exception as e:
                print(f'{str(e)}: {href}')
   
    return abs_path_list

def get_images_from_html(html: str, base_url: str):
    soup = BeautifulSoup(html, 'html.parser')
    image_path_list = []

    img_tag_list = soup.find_all('img')

    for item in img_tag_list:
        if not isinstance(item, Tag):
            continue
        src = item.get('src')
        if isinstance(src, str) and src:
            try:
                image_path_list.append(urljoin(base_url, src))
            except Exception as e:
                print(f'{str(e)}: {src}')

    return image_path_list
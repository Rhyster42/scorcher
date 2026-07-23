import re, requests
from urllib.parse import urlsplit, urljoin
from bs4 import BeautifulSoup, Tag

from typing import TypedDict


class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]

def normalize_url(url: str) -> str:
    parts = urlsplit(url)
    domain = parts.netloc
    path = parts.path

    path = path.rstrip('/')
    
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

    if not isinstance(p_tag, Tag):
        return ""

    text = p_tag.get_text()
    return re.sub(r'\s+', ' ', text).strip()

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

def extract_page_data(html:str, page_url: str):
    page_data: PageData = {
        'url': page_url,
        'heading': get_heading_from_html(html),
        'first_paragraph': get_first_paragraph_from_html(html),
        'outgoing_links': get_urls_from_html(html, page_url),
        'image_urls': get_images_from_html(html, page_url)
    }

    return page_data

def get_html(url: str) -> str:
    response = requests.get(url, headers={"User-Agent": "BootCrawler/1.0"})

    if response.status_code >= 400:
        raise Exception("Request failed")
    if 'text/html' not in response.headers['Content-Type']:
        raise Exception(f'Incorrect content type: {response.headers["Content-Type"]}')
    if response.status_code != 200:
        raise Exception(f'Error: {response.status_code} - {response.raise_for_status}')
    return response.text

def crawl_page(base_url: str, current_url=None, page_data=None):
    if current_url is None:
        current_url = base_url
    if page_data is None:
        page_data = PageData = {}


    nm_base_url = normalize_url(base_url)
    nm_current_url = normalize_url(current_url)

    if nm_base_url != nm_current_url:
        return
    
    if nm_current_url in page_data:
        return
    
    html = get_html(current_url)
    print(html)

    new_page_data = extract_page_data(html, nm_current_url)
    page_data[nm_current_url] = new_page_data
    
    page_urls = new_page_data['outgoing_links']

    for url in page_urls:
        crawl_page(nm_base_url, url, page_data)

    return
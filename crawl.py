import re, requests, asyncio, aiohttp
from urllib.parse import urlsplit, urljoin
from bs4 import BeautifulSoup, Tag
from types import TracebackType

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

class AsyncCrawler:
    def __init__(self, base_url:str, max_concur: int, max_pgs: int) -> None:
        self.base_url = base_url
        self.base_domain = urlsplit(base_url).netloc
        self.page_data: dict[str, PageData] = {}
        self.lock = asyncio.Lock()
        self.max_concurrency = max_concur
        self.semaphore = asyncio.Semaphore(self.max_concurrency)
        self.session: aiohttp.ClientSession | None = None
        self.max_pages = max_pgs
        self.should_stop = False
        self.all_tasks: set[asyncio.Task[None]] = set()

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(
            self,
            exc_type: type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None,
        ) ->  None:
        if self.session is not None:
            await self.session.close()

    async def add_page_visit(self, normalized_url: str) -> bool:
        async with self.lock:
            if self.should_stop:
                return False
            if normalized_url in self.page_data:
                return False
            
            if len(self.page_data) >= self.max_pages:
                self.should_stop = True
                print('Reached maximum number of pages to crawl.')
                for task in self.all_tasks:
                    if not task.done():
                        task.cancel()
                return False
            return True
            
    async def get_html(self, url: str) -> str:
        if self.session is None:
            return None
        try:
            async with self.session.get(
                url, headers={"User-Agent": "BootCrawler/1.0"}
            ) as response:
                if response.status > 399:
                    print(f'Error: HTTP {response.status} for {url}')
                    return None
                
                content_type = response.headers.get("content-type", "")
                if "text/html" not in content_type:
                    print(f"Error: Non-HTML content {content_type} for {url}")
                    return None
                
                return await response.text()
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    async def crawl_page(self, current_url: str) -> None:
        if self.should_stop:
            return

        current_url_obj = urlsplit(current_url)
        if current_url_obj.netloc != self.base_domain:
            return
            
        normalized_url = normalize_url(current_url)

        is_new_page = await self.add_page_visit(normalized_url)
        if not is_new_page:
            return
            
        async with self.semaphore:
            print(f'Now crawling {current_url} (total concurrent crawlers:{self.max_concurrency - self.semaphore._value})')
            html = await self.get_html(current_url)
            if html is None:
                return
                
            new_page_data = extract_page_data(html, current_url)
            async with self.lock:
                self.page_data[normalized_url] = new_page_data

            new_page_urls = get_urls_from_html(html, self.base_url)

        if self.should_stop:
            return

        tasks:list[asyncio.Task[None]] = []
        for next_url in new_page_urls:
            task = asyncio.create_task(self.crawl_page(next_url))
            tasks.append(task)
            self.all_tasks.add(task)

        if tasks:
            try:
                await asyncio.gather(*tasks, return_exceptions=True)
            finally:
                for task in tasks:
                    self.all_tasks.discard(task)

    async def crawl(self) -> dict[str, PageData]:
        await self.crawl_page(self.base_url)
        return self.page_data
    
async def crawl_site_async(base_url: str, max_concur: int, max_pgs: int):
    async with AsyncCrawler(base_url, max_concur, max_pgs) as crawler:
        return await crawler.crawl()


        


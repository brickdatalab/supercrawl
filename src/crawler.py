import asyncio
import logging
from urllib.parse import urlparse, urljoin
import aiohttp
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from src.settings_manager import settings, supabase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Crawler:
    def __init__(self, project_id, base_url, max_depth=2, max_pages=100):
        self.project_id = project_id
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.visited = set()
        self.queue = asyncio.Queue()
        self.crawl_id = None

    async def start(self):
        logger.info(f"Starting crawl for {self.base_url}")
        
        # Create crawl record
        crawl_data = {
            "project_id": self.project_id,
            "status": "running",
            "total_pages": 0
        }
        response = supabase.table("crawls").insert(crawl_data).execute()
        self.crawl_id = response.data[0]['id']
        
        await self.queue.put((self.base_url, 0))
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            
            while not self.queue.empty() and len(self.visited) < self.max_pages:
                url, depth = await self.queue.get()
                
                if url in self.visited or depth > self.max_depth:
                    continue
                
                self.visited.add(url)
                await self.process_page(context, url, depth)
                
            await browser.close()
        
        # Update crawl status
        supabase.table("crawls").update({
            "status": "completed",
            "total_pages": len(self.visited),
            "completed_at": "now()"
        }).eq("id", self.crawl_id).execute()
        
        logger.info(f"Crawl completed. Visited {len(self.visited)} pages.")
        return len(self.visited)

    async def process_page(self, context, url, depth):
        logger.info(f"Processing {url} at depth {depth}")
        try:
            page = await context.new_page()
            start_time = asyncio.get_event_loop().time()
            await page.goto(url, wait_until="networkidle", timeout=30000)
            load_time_ms = int((asyncio.get_event_loop().time() - start_time) * 1000)
            
            content = await page.content()
            title = await page.title()
            
            # Basic extraction
            soup = BeautifulSoup(content, 'html.parser')
            meta_desc = soup.find("meta", attrs={"name": "description"})
            meta_description = meta_desc["content"] if meta_desc else None
            h1 = soup.find("h1").get_text().strip() if soup.find("h1") else None
            
            # Save page to Supabase
            page_data = {
                "crawl_id": self.crawl_id,
                "url": url,
                "title": title,
                "meta_description": meta_description,
                "h1": h1,
                "status_code": 200, # Playwright doesn't give status easily in goto, assuming 200 if no error
                "content_text": soup.get_text(),
                "load_time_ms": load_time_ms
            }
            page_res = supabase.table("pages").insert(page_data).execute()
            page_id = page_res.data[0]['id']
            
            # Trigger AI processing
            from src.celery_worker import celery_app
            celery_app.send_task("src.tasks.process_page_ai_task", args=[page_id, soup.get_text()])
            
            # Trigger SEO Analysis
            seo_data = {
                "title": title,
                "meta_description": meta_description,
                "h1": h1,
                "load_time_ms": load_time_ms
            }
            celery_app.send_task("src.tasks.analyze_page_seo_task", args=[page_id, seo_data])
            
            links = self.extract_links(soup, url)
            
            # Save links
            links_data = []
            for link in links:
                links_data.append({
                    "source_page_id": page_id,
                    "target_url": link,
                    "type": "internal" # Simplified for now
                })
                
                if link not in self.visited:
                    await self.queue.put((link, depth + 1))
            
            if links_data:
                supabase.table("links").insert(links_data).execute()
                    
            await page.close()
            
        except Exception as e:
            logger.error(f"Error processing {url}: {e}")
            # Log error page?

    def extract_links(self, soup, base_url):
        links = set()
        for a in soup.find_all('a', href=True):
            href = a['href']
            full_url = urljoin(base_url, href)
            parsed = urlparse(full_url)
            
            # Only internal links for now
            if parsed.netloc == self.domain:
                links.add(full_url)
        return list(links)

if __name__ == "__main__":
    # Test run
    async def main():
        # You need a valid project_id from Supabase to run this
        print("Run via Celery or provide project_id")

    asyncio.run(main())

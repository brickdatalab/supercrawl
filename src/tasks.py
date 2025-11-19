import asyncio
from src.celery_worker import celery_app
from src.crawler import Crawler
from src.ai_processor import ai_processor
from src.seo_analyzer import SEOAnalyzer
from src.settings_manager import supabase

@celery_app.task
def start_crawl_task(project_id):
    from src.crawler import Crawler
    # Fetch project details to get base_url
    # For now assuming we pass base_url or fetch it here. 
    # But Crawler init needs base_url. 
    # Let's fetch project from Supabase
    project = supabase.table("projects").select("url").eq("id", project_id).execute()
    if project.data:
        base_url = project.data[0]['url']
        crawler = Crawler(project_id, base_url)
        asyncio.run(crawler.start())
    else:
        print(f"Project {project_id} not found")

@celery_app.task
def process_page_ai_task(page_id, content_text):
    asyncio.run(ai_processor.process_page(page_id, content_text))

@celery_app.task
def analyze_page_seo_task(page_id, page_data):
    """
    Analyze a page for SEO issues and save to Supabase.
    page_data should be a dict with keys: title, meta_description, h1, load_time_ms
    """
    issues = SEOAnalyzer.analyze(page_data)
    
    if issues:
        # Add page_id to each issue
        for issue in issues:
            issue['page_id'] = page_id
            
        try:
            supabase.table("issues").insert(issues).execute()
        except Exception as e:
            print(f"Error saving issues for page {page_id}: {e}")


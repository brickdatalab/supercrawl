from flask import Flask, jsonify, request
from flask_cors import CORS
from src.settings_manager import settings, supabase
from src.tasks import start_crawl_task

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = settings.SECRET_KEY

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "service": "SuperCrawl API"})

@app.route('/projects', methods=['POST'])
def create_project():
    data = request.json
    user_id = data.get('user_id') # In prod, get from auth token
    domain = data.get('domain')
    
    if not domain:
        return jsonify({"error": "Domain is required"}), 400
        
    res = supabase.table("projects").insert({
        "user_id": user_id,
        "domain": domain
    }).execute()
    
    return jsonify(res.data[0]), 201

@app.route('/projects/<project_id>/crawl', methods=['POST'])
def start_crawl(project_id):
    # Verify project exists
    proj = supabase.table("projects").select("*").eq("id", project_id).execute()
    if not proj.data:
        return jsonify({"error": "Project not found"}), 404
        
    project = proj.data[0]
    base_url = project['domain']
    if not base_url.startswith('http'):
        base_url = f"https://{base_url}"
        
    # Start Celery task
    task = start_crawl_task.delay(project_id, base_url)
    
    return jsonify({"message": "Crawl started", "task_id": task.id}), 202

@app.route('/projects/<project_id>/pages', methods=['GET'])
def get_pages(project_id):
    # Get latest crawl
    crawls = supabase.table("crawls").select("id").eq("project_id", project_id).order("created_at", desc=True).limit(1).execute()
    
    if not crawls.data:
        return jsonify([]), 200
        
    crawl_id = crawls.data[0]['id']
    
    pages = supabase.table("pages").select("*").eq("crawl_id", crawl_id).execute()
    return jsonify(pages.data), 200

@app.route('/projects', methods=['GET'])
def list_projects():
    # In prod, filter by user_id
    projects = supabase.table("projects").select("*").execute()
    return jsonify(projects.data), 200

@app.route('/projects/<project_id>/issues', methods=['GET'])
def get_issues(project_id):
    # Get latest crawl
    crawls = supabase.table("crawls").select("id").eq("project_id", project_id).order("created_at", desc=True).limit(1).execute()
    
    if not crawls.data:
        return jsonify([]), 200
        
    crawl_id = crawls.data[0]['id']
    
    # Get all pages for this crawl
    pages_res = supabase.table("pages").select("id, url, title").eq("crawl_id", crawl_id).execute()
    pages_map = {p['id']: p for p in pages_res.data}
    page_ids = list(pages_map.keys())
    
    if not page_ids:
        return jsonify([]), 200

    # Get issues for these pages
    issues = supabase.table("issues").select("*").in_("page_id", page_ids).execute()
    
    # Enrich issues with page url/title
    enriched_issues = []
    for issue in issues.data:
        page = pages_map.get(issue['page_id'])
        if page:
            issue['url'] = page['url']
            issue['page_title'] = page['title']
            enriched_issues.append(issue)
            
    return jsonify(enriched_issues), 200

if __name__ == '__main__':
    app.run(debug=settings.DEBUG, port=5000)

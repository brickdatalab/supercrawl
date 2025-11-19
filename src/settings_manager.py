import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

class Settings:
    # Supabase
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    
    # Google Gemini
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    # Google PageSpeed
    PAGESPEED_API_KEY = os.getenv("PAGESPEED_API_KEY")
    
    # Redis / Celery
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # App
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    DEBUG = os.getenv("FLASK_DEBUG", "True") == "True"

settings = Settings()
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

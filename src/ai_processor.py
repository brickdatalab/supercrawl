import google.generativeai as genai
from src.settings_manager import settings, supabase
import logging

logger = logging.getLogger(__name__)

# Configure Gemini
genai.configure(api_key=settings.GOOGLE_API_KEY)

class AIProcessor:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-pro')
        self.embedding_model = 'models/embedding-001'

    async def process_page(self, page_id, content_text):
        """
        Generate embeddings and analysis for a page.
        """
        try:
            # 1. Generate Embeddings (Chunking)
            chunks = self.chunk_text(content_text)
            embeddings_data = []
            
            for chunk in chunks:
                embedding = genai.embed_content(
                    model=self.embedding_model,
                    content=chunk,
                    task_type="retrieval_document"
                )
                
                embeddings_data.append({
                    "page_id": page_id,
                    "content_chunk": chunk,
                    "embedding": embedding['embedding']
                })
            
            if embeddings_data:
                supabase.table("page_embeddings").insert(embeddings_data).execute()
                
            # 2. Generate Summary & Sentiment (Optional, can be separate)
            # ...
            
            return True
        except Exception as e:
            logger.error(f"Error processing page {page_id}: {e}")
            return False

    def chunk_text(self, text, chunk_size=1000):
        """
        Simple chunking. In production, use a proper tokenizer or sentence splitter.
        """
        return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

ai_processor = AIProcessor()

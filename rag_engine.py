import os
import pypdf
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document
import shutil

# Constants
PERSIST_DIRECTORY = "./chroma_db"
EMBEDDING_MODEL_NAME = "nomic-embed-text"

class RAGEngine:
    def __init__(self):
        self.embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL_NAME)
        self.vector_store = None
        self._initialize_vector_store()

    def _initialize_vector_store(self):
        """Initializes the ChromaDB vector store."""
        # Check if vector store exists, if not create it
        self.vector_store = Chroma(
            persist_directory=PERSIST_DIRECTORY,
            embedding_function=self.embeddings
        )

    def parse_pdf(self, file) -> str:
        """Extracts text from a PDF file object."""
        try:
            pdf_reader = pypdf.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
            return text
        except Exception as e:
            print(f"Error parsing PDF: {e}")
            return ""

    def add_jd_to_store(self, jd_text: str, jd_id: str = "current_jd"):
        """Adds or updates the Job Description in the vector store."""
        # Clear existing JD with the same ID to ensure we only compare against the current one
        # Note: Chroma doesn't have a direct 'delete by metadata' easily exposed in all versions, 
        # but we can just add it and retrieval will find it. 
        # For a cleaner approach in this simple app, we might want to reset the DB or just use a specific collection.
        # For now, we'll just add it.
        
        # A better approach for this specific "Gatekeeper" flow might be to not even persist the JD 
        # if we only compare 1:1 at runtime, but using a vector store allows for future scalability 
        # (e.g. matching against multiple open positions).
        
        doc = Document(page_content=jd_text, metadata={"type": "jd", "id": jd_id})
        self.vector_store.add_documents([doc])
        # self.vector_store.persist() # Chroma 0.4+ persists automatically

    def calculate_match_score(self, resume_text: str, jd_text: str) -> float:
        """
        Calculates a semantic similarity score between the resume and the JD.
        Returns a float between 0 and 1.
        """
        if not resume_text or not jd_text:
            return 0.0

        # We can use the vector store to do a similarity search, 
        # OR since we have the text right here, we can just compute cosine similarity directly 
        # using the embeddings. This is often faster and more direct for 1:1 comparison.
        
        resume_embedding = self.embeddings.embed_query(resume_text)
        jd_embedding = self.embeddings.embed_query(jd_text)
        
        # Compute Cosine Similarity manually or use a utility
        import numpy as np
        
        def cosine_similarity(a, b):
            return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
            
        score = cosine_similarity(resume_embedding, jd_embedding)
        
        # Normalize/Clip if necessary (usually -1 to 1, but for text it's mostly 0 to 1)
        return max(0.0, min(1.0, float(score)))

    def query_vector_store(self, query: str, k: int = 3):
        """Queries the vector store for relevant context (e.g. from the JD)."""
        return self.vector_store.similarity_search(query, k=k)

# Singleton instance for easy import
rag_engine = RAGEngine()

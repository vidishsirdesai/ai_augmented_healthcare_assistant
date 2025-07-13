# src/core/config.py
import os

class Settings:
    # Ollama configuration
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "mistral")

    # ChromaDB configuration
    CHROMADB_PATH: str = os.getenv("CHROMADB_PATH", "./chroma_db")

    # Embedding model
    EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"

    # Data paths
    DATA_DIR: str = os.getenv("DATA_DIR", "./data")
    PATIENT_RECORDS_PATH: str = os.path.join(DATA_DIR, "patient_records.json")
    TREATMENT_GUIDES_PATH: str = os.path.join(DATA_DIR, "treatment_guides.json")
    DRUG_INTERACTIONS_PATH: str = os.path.join(DATA_DIR, "drug_interactions.json")

settings = Settings()

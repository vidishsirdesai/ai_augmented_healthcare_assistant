# backend/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os

from api.endpoints import router
from core.rag_cag_pipeline import RAGCAGPipeline
from core.data_loader import DataLoader
from core.config import settings

app = FastAPI(
    title="AI Augmented Healthcare Assistant",
    description="LLM powered chat assistant for doctors with RAG and CAG capabilities."
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Mount static files
app.mount("/static", StaticFiles(directory="backend/static"), name="static")

# Global instance for the RAG/CAG pipeline
rag_cag_pipeline: RAGCAGPipeline = None

@app.on_event("startup")
async def startup_event():
    """
    Initializes the RAG/CAG pipeline and loads data into ChromaDB on application startup.
    """
    global rag_cag_pipeline
    try:
        data_loader = DataLoader()
        patient_records = data_loader.load_data(settings.PATIENT_RECORDS_PATH)
        treatment_guides = data_loader.load_data(settings.TREATMENT_GUIDES_PATH)
        drug_interactions = data_loader.load_data(settings.DRUG_INTERACTIONS_PATH)

        rag_cag_pipeline = RAGCAGPipeline()
        await rag_cag_pipeline.initialize() # Connect to Ollama and check ChromaDB

        if not rag_cag_pipeline.is_chroma_initialized():
            print("ChromaDB is empty or not initialized. Ingesting data...")
            rag_cag_pipeline.ingest_data(patient_records, "patient_records")
            rag_cag_pipeline.ingest_data(treatment_guides, "treatment_guides")
            rag_cag_pipeline.ingest_data(drug_interactions, "drug_interactions")
            print("Data ingestion complete.")
        else:
            print("ChromaDB already contains data. Skipping ingestion.")

    except Exception as e:
        print(f"Failed to initialize RAG/CAG pipeline or load data: {e}")
        # In a production system, you might want to log this more formally
        # and potentially exit the application if core services fail.
        raise HTTPException(status_code=500, detail=f"Server startup failed: {e}")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """
    Serves the main HTML page.
    """
    with open("backend/static/index.html", "r") as f:
        return HTMLResponse(content=f.read())

# Include API endpoints
app.include_router(router)

# Expose the pipeline for endpoints to use
def get_rag_cag_pipeline() -> RAGCAGPipeline:
    if rag_cag_pipeline is None:
        raise HTTPException(status_code=500, detail="RAG/CAG Pipeline not initialized.")
    return rag_cag_pipeline
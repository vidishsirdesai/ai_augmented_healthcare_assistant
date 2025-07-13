# src/main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os

from src.core.rag_cag_pipeline import RAGCAGPipeline
from src.core.data_loader import DataLoader
from src.core.config import settings

app = FastAPI(
    title="AI Augmented Healthcare Assistant",
    description="LLM powered chat assistant for doctors with RAG and CAG capabilities."
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="src/static"), name="static")

# Global instance for the RAG/CAG pipeline
rag_cag_pipeline: RAGCAGPipeline = None

# Define the dependency getter function
def get_rag_cag_pipeline_dependency() -> RAGCAGPipeline:
    if rag_cag_pipeline is None:
        raise HTTPException(status_code=500, detail="RAG/CAG Pipeline not initialized.")
    return rag_cag_pipeline

# Now import the router after the dependency is defined
from src.api.endpoints import router as api_router


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
        await rag_cag_pipeline.initialize() # This initializes LLM, Embeddings, Chroma Client

        # Check if ChromaDB is populated BEFORE attempting ingestion
        if not rag_cag_pipeline.is_chroma_initialized_and_populated(): # Use the new method
            print("ChromaDB is empty or not initialized. Ingesting data...")
            rag_cag_pipeline.ingest_data(patient_records, "patient_records")
            rag_cag_pipeline.ingest_data(treatment_guides, "treatment_guides")
            rag_cag_pipeline.ingest_data(drug_interactions, "drug_interactions")
            print("Data ingestion complete.")
            # ONLY setup QA chain AFTER data is confirmed to be ingested
            rag_cag_pipeline._setup_qa_chain() # Call setup explicitly here
        else:
            print("ChromaDB already contains data. Setting up QA chain.")
            rag_cag_pipeline._setup_qa_chain() # Setup QA chain if DB was already populated

    except Exception as e:
        print(f"Failed to initialize RAG/CAG pipeline or load data: {e}")
        raise HTTPException(status_code=500, detail=f"Server startup failed: {e}")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """
    Serves the main HTML page.
    """
    with open("src/static/index.html", "r") as f:
        return HTMLResponse(content=f.read())

# Include API endpoints
app.include_router(api_router)

# Expose the pipeline for endpoints to use
def get_rag_cag_pipeline() -> RAGCAGPipeline:
    if rag_cag_pipeline is None:
        raise HTTPException(status_code=500, detail="RAG/CAG Pipeline not initialized.")
    return rag_cag_pipeline
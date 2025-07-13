# backend/api/endpoints.py
from fastapi import APIRouter, HTTPException, Depends
from api.models import ChatQuery, ChatResponse
from core.rag_cag_pipeline import RAGCAGPipeline
from main import get_rag_cag_pipeline # Import the getter function

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_with_assistant(
    chat_query: ChatQuery,
    rag_cag_pipeline: RAGCAGPipeline = Depends(get_rag_cag_pipeline)
):
    """
    Receives a natural language query from the doctor and returns a comprehensive response.
    """
    try:
        response, sources = await rag_cag_pipeline.process_query(chat_query.query)
        return ChatResponse(response=response, source_documents=sources)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

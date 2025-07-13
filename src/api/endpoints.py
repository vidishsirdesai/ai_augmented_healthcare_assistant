# src/api/endpoints.py
from fastapi import APIRouter, HTTPException, Depends
from src.api.models import ChatQuery, ChatResponse
from src.core.rag_cag_pipeline import RAGCAGPipeline

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_with_assistant(
    chat_query: ChatQuery,
    # Corrected access: import 'src.main' then get the attribute from the returned module
    rag_cag_pipeline_instance: RAGCAGPipeline = Depends(lambda: __import__("src.main").main.get_rag_cag_pipeline_dependency())
):
    """
    Receives a natural language query from the doctor and returns a comprehensive response.
    """
    try:
        response, sources = await rag_cag_pipeline_instance.process_query(chat_query.query)
        return ChatResponse(response=response, source_documents=sources)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

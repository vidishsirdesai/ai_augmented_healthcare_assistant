# backend/api/models.py
from pydantic import BaseModel, Field

class ChatQuery(BaseModel):
    query: str = Field(..., min_length=1, example="What is the treatment for Type 2 Diabetes for patient Alice Smith?")

class ChatResponse(BaseModel):
    response: str = Field(..., example="The recommended treatment for Type 2 Diabetes involves lifestyle changes and Metformin.")
    source_documents: list[dict] = Field(default_factory=list, example=[{"content": "...", "metadata": {"source": "patient_records", "id": "P001"}}])

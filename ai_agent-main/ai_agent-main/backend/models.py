from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    mode: str  # "scientific_idea" or "general"

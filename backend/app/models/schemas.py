from pydantic import BaseModel


class Query(BaseModel):
    """Schema for query requests."""
    question: str


class Response(BaseModel):
    """Schema for query responses."""
    answer: str

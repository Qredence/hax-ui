from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class MessageRole(str, Enum):
    """Message role enum"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatMessage(BaseModel):
    """Chat message schema"""
    role: MessageRole
    content: str
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)
    thoughts: Optional[str] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ChatRequest(BaseModel):
    """Chat request schema"""
    message: str = Field(..., min_length=1, max_length=10000, description="The message to send")
    history: List[ChatMessage] = Field(default_factory=list, description="Conversation history")
    thinking_mode: bool = Field(default=False, description="Enable thinking mode for detailed reasoning")


class ChatResponse(BaseModel):
    """Chat response schema"""
    content: str = Field(..., description="The assistant's response")
    thoughts: Optional[str] = Field(None, description="Assistant's reasoning process (if thinking mode enabled)")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class StreamChunk(BaseModel):
    """Streaming response chunk"""
    content: Optional[str] = Field(None, description="Text content chunk")
    thoughts: Optional[str] = Field(None, description="Thoughts content chunk")
    is_final: bool = Field(default=False, description="Whether this is the final chunk")


class ErrorResponse(BaseModel):
    """Error response schema"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    code: Optional[str] = Field(None, description="Error code")
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from typing import List
import asyncio
import json
import logging

from app.schemas.chat import ChatRequest, ChatResponse, StreamChunk, ErrorResponse
from app.services.gemini import GeminiService

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize Gemini service
gemini_service = GeminiService()


@router.post(
    "/messages",
    response_model=ChatResponse,
    summary="Send chat message",
    description="Send a chat message and receive a response from the AI assistant"
)
async def send_message(request: ChatRequest):
    """
    Send a chat message and get AI response
    
    - **message**: The message content to send
    - **history**: Optional conversation history for context
    - **thinking_mode**: Enable to see the assistant's reasoning process
    """
    try:
        response = await gemini_service.generate_response(
            message=request.message,
            history=request.history,
            thinking_mode=request.thinking_mode
        )
        
        return ChatResponse(
            content=response["content"],
            thoughts=response.get("thoughts")
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Configuration error: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error in send_message: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate response: {str(e)}"
        )


@router.post(
    "/messages/stream",
    summary="Stream chat message",
    description="Send a chat message and receive a streaming response from the AI assistant"
)
async def stream_message(request: ChatRequest):
    """
    Stream chat response using Server-Sent Events
    
    - **message**: The message content to send
    - **history**: Optional conversation history for context  
    - **thinking_mode**: Enable to see the assistant's reasoning process
    
    Returns a streaming response with content chunks as they are generated.
    """
    try:
        async def generate():
            try:
                async for chunk in gemini_service.stream_response(
                    message=request.message,
                    history=request.history,
                    thinking_mode=request.thinking_mode
                ):
                    # Format as Server-Sent Events
                    chunk_data = StreamChunk(**chunk)
                    yield f"data: {chunk_data.model_dump_json()}\n\n"
                    
                    if chunk.get("is_final", False):
                        break
                        
            except Exception as e:
                logger.error(f"Error in stream generation: {e}")
                error_chunk = StreamChunk(
                    content=f"Error: {str(e)}",
                    is_final=True
                )
                yield f"data: {error_chunk.model_dump_json()}\n\n"
        
        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
            }
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Configuration error: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error in stream_message: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start streaming: {str(e)}"
        )


@router.get(
    "/health",
    summary="Chat service health check",
    description="Check if the chat service is healthy and properly configured"
)
async def chat_health_check():
    """
    Health check for chat service
    """
    try:
        # Simple test to verify Gemini service configuration
        gemini_service._ensure_init()
        return {
            "status": "healthy",
            "service": "chat",
            "gemini_model": gemini_service.model_id
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Chat service unhealthy: {str(e)}"
        )
import asyncio
import json
import logging
from typing import AsyncGenerator, Dict, List, Optional
import google.generativeai as genai
from google.generativeai.types import GenerateContentResponse

from app.config import settings
from app.schemas.chat import ChatMessage, MessageRole

logger = logging.getLogger(__name__)


class GeminiService:
    """Service for interacting with Google Gemini API"""
    
    def __init__(self):
        """Initialize Gemini service"""
        self.api_key = settings.gemini_api_key
        self.model_id = settings.gemini_model_id
        self.model = None
        self._initialized = False
        
    def _ensure_init(self):
        """Ensure the service is initialized"""
        if self._initialized:
            return
            
        if not self.api_key:
            raise ValueError("Gemini API key not configured")
        
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_id)
            self._initialized = True
            logger.info(f"Gemini service initialized with model: {self.model_id}")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini service: {e}")
            raise ValueError(f"Failed to initialize Gemini service: {e}")
    
    def _convert_messages_to_gemini_format(self, messages: List[ChatMessage]) -> List[Dict]:
        """Convert chat messages to Gemini format"""
        gemini_messages = []
        
        for msg in messages:
            role = "user" if msg.role == MessageRole.USER else "model"
            gemini_messages.append({
                "role": role,
                "parts": [{"text": msg.content}]
            })
        
        return gemini_messages
    
    async def generate_response(
        self,
        message: str,
        history: List[ChatMessage] = None,
        thinking_mode: bool = False
    ) -> Dict[str, str]:
        """Generate a single response (non-streaming)"""
        self._ensure_init()
        
        if history is None:
            history = []
        
        try:
            # Convert messages to Gemini format
            messages = history + [ChatMessage(role=MessageRole.USER, content=message)]
            gemini_messages = self._convert_messages_to_gemini_format(messages)
            
            # Configure generation parameters
            generation_config = {
                "temperature": 0.7,
                "max_output_tokens": 2048,
                "top_p": 0.8,
                "top_k": 10,
            }
            
            # Add thinking config if requested
            request_config = {
                "contents": gemini_messages,
                "generation_config": generation_config,
            }
            
            if thinking_mode:
                request_config["config"] = {
                    "thinking_config": {
                        "include_thoughts": True,
                    }
                }
            
            # Generate response
            response = await asyncio.to_thread(
                self.model.generate_content,
                **request_config
            )
            
            # Extract content and thoughts
            content = ""
            thoughts = ""
            
            if response.candidates and response.candidates[0].content:
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'thought') and part.thought:
                        thoughts += part.text
                    else:
                        content += part.text
            
            return {
                "content": content,
                "thoughts": thoughts if thinking_mode else None
            }
            
        except Exception as e:
            logger.error(f"Error generating Gemini response: {e}")
            raise Exception(f"Failed to generate response: {str(e)}")
    
    async def stream_response(
        self,
        message: str,
        history: List[ChatMessage] = None,
        thinking_mode: bool = False
    ) -> AsyncGenerator[Dict[str, str], None]:
        """Generate streaming response"""
        self._ensure_init()
        
        if history is None:
            history = []
        
        try:
            # Convert messages to Gemini format
            messages = history + [ChatMessage(role=MessageRole.USER, content=message)]
            gemini_messages = self._convert_messages_to_gemini_format(messages)
            
            # Configure generation parameters
            generation_config = {
                "temperature": 0.7,
                "max_output_tokens": 2048,
                "top_p": 0.8,
                "top_k": 10,
            }
            
            # Add thinking config if requested
            request_config = {
                "contents": gemini_messages,
                "generation_config": generation_config,
            }
            
            if thinking_mode:
                request_config["config"] = {
                    "thinking_config": {
                        "include_thoughts": True,
                    }
                }
            
            # Generate streaming response
            response_stream = await asyncio.to_thread(
                self.model.generate_content,
                stream=True,
                **request_config
            )
            
            # Process streaming chunks
            for chunk in response_stream:
                if chunk.candidates and chunk.candidates[0].content:
                    content_chunk = ""
                    thoughts_chunk = ""
                    
                    for part in chunk.candidates[0].content.parts:
                        if hasattr(part, 'thought') and part.thought:
                            thoughts_chunk += part.text
                        else:
                            content_chunk += part.text
                    
                    if content_chunk or thoughts_chunk:
                        yield {
                            "content": content_chunk,
                            "thoughts": thoughts_chunk if thinking_mode else None,
                            "is_final": False
                        }
            
            # Send final chunk
            yield {
                "content": "",
                "thoughts": None,
                "is_final": True
            }
            
        except Exception as e:
            logger.error(f"Error in Gemini streaming: {e}")
            yield {
                "content": f"Error: {str(e)}",
                "thoughts": None,
                "is_final": True
            }
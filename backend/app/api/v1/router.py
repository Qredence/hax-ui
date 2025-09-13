from fastapi import APIRouter

from app.api.v1 import chat

# Create main API router
api_router = APIRouter()

# Include sub-routers
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])

# Health check endpoint
@api_router.get("/health")
async def health_check():
    """API health check"""
    return {"status": "healthy", "service": "hax-ui-api"}
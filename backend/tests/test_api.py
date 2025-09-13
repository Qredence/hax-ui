import pytest
from fastapi.testclient import TestClient
import os
from unittest.mock import patch

# Set test environment before importing app modules
os.environ["PYTEST_CURRENT_TEST"] = "test"

from app.main import create_app
from app.config import Settings

# Test configuration
test_settings = Settings(
    secret_key="test-secret-key",
    database_url="sqlite:///./test.db",
    gemini_api_key="test-gemini-key",
    debug=True,
    allowed_origins=["http://localhost:3000"]
)


@pytest.fixture
def app():
    """Create a test app instance"""
    with patch("app.main.settings", test_settings):
        app = create_app()
        yield app


@pytest.fixture
def client(app):
    """Create a test client"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def setup_test_env():
    """Setup test environment variables"""
    test_env = {
        "SECRET_KEY": "test-secret-key",
        "DATABASE_URL": "sqlite:///./test.db",
        "GEMINI_API_KEY": "test-gemini-key",
        "DEBUG": "true"
    }
    
    with patch.dict(os.environ, test_env):
        yield


class TestHealthEndpoints:
    """Test health check endpoints"""
    
    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "HAX UI API"
        assert "version" in data
        assert "docs" in data
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
    
    def test_api_health_check(self, client):
        """Test API health check endpoint"""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "hax-ui-api"


class TestChatEndpoints:
    """Test chat endpoints"""
    
    @patch("app.services.gemini.GeminiService._ensure_init")
    @patch("app.services.gemini.GeminiService.generate_response")
    def test_send_message_success(self, mock_generate, mock_init, client):
        """Test successful message sending"""
        # Mock the Gemini service response
        mock_generate.return_value = {
            "content": "Hello! How can I help you?",
            "thoughts": None
        }
        
        response = client.post(
            "/api/v1/chat/messages",
            json={
                "message": "Hello",
                "history": [],
                "thinking_mode": False
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["content"] == "Hello! How can I help you?"
        assert "timestamp" in data
    
    def test_send_message_empty_message(self, client):
        """Test sending empty message"""
        response = client.post(
            "/api/v1/chat/messages",
            json={
                "message": "",
                "history": [],
                "thinking_mode": False
            }
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_send_message_with_history(self, client):
        """Test sending message with conversation history"""
        with patch("app.services.gemini.GeminiService._ensure_init"), \
             patch("app.services.gemini.GeminiService.generate_response") as mock_generate:
            
            mock_generate.return_value = {
                "content": "Based on our previous conversation...",
                "thoughts": None
            }
            
            response = client.post(
                "/api/v1/chat/messages",
                json={
                    "message": "Continue our discussion",
                    "history": [
                        {
                            "role": "user",
                            "content": "Hello",
                            "timestamp": "2024-01-01T00:00:00Z"
                        },
                        {
                            "role": "assistant", 
                            "content": "Hi there!",
                            "timestamp": "2024-01-01T00:00:01Z"
                        }
                    ],
                    "thinking_mode": False
                }
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "content" in data
    
    @patch("app.services.gemini.GeminiService._ensure_init")
    def test_chat_health_check_success(self, mock_init, client):
        """Test chat service health check when healthy"""
        response = client.get("/api/v1/chat/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "chat"
    
    @patch("app.services.gemini.GeminiService._ensure_init")
    def test_chat_health_check_failure(self, mock_init, client):
        """Test chat service health check when unhealthy"""
        mock_init.side_effect = Exception("Configuration error")
        
        response = client.get("/api/v1/chat/health")
        assert response.status_code == 503
        data = response.json()
        assert "Chat service unhealthy" in data["detail"]


class TestChatSchemas:
    """Test chat schema validation"""
    
    def test_chat_request_validation(self, client):
        """Test chat request schema validation"""
        # Test message too long
        response = client.post(
            "/api/v1/chat/messages",
            json={
                "message": "x" * 10001,  # Exceeds max length
                "history": [],
                "thinking_mode": False
            }
        )
        assert response.status_code == 422
    
    def test_chat_request_missing_fields(self, client):
        """Test missing required fields"""
        response = client.post(
            "/api/v1/chat/messages",
            json={}
        )
        assert response.status_code == 422
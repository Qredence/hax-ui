# HAX UI Backend API

A FastAPI-powered backend for the HAX UI chat interface, providing AI-powered conversations with Google Gemini integration.

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) - Fast Python package manager
- Optional: PostgreSQL for production

### Installation

1. **Install uv** (if not already installed):

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Navigate to backend directory:**

   ```bash
   cd backend
   ```

3. **Run the startup script:**

   ```bash
   ./start.sh
   ```

   Or manually with uv:

   ```bash
   # Sync dependencies with uv
   uv sync --dev

   # Copy environment configuration
   cp .env.example .env
   # Edit .env with your configuration

   # Start server with uv
   uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

4. **Configure environment variables** in `.env`:

   ```bash
   SECRET_KEY=your-secret-key-here
   GEMINI_API_KEY=your-gemini-api-key-here
   DATABASE_URL=postgresql://user:pass@localhost:5432/haxui  # Optional
   ```

5. **Access the API:**
   - API Server: http://localhost:8000
   - Interactive Docs: http://localhost:8000/api/v1/docs
   - ReDoc: http://localhost:8000/api/v1/redoc

## 📚 API Endpoints

### Health Checks

- `GET /` - Root endpoint with API information
- `GET /health` - General health check
- `GET /api/v1/health` - API health check
- `GET /api/v1/chat/health` - Chat service health check

### Chat Endpoints

#### Send Message

```http
POST /api/v1/chat/messages
Content-Type: application/json

{
  "message": "Hello, how are you?",
  "history": [
    {
      "role": "user",
      "content": "Previous message",
      "timestamp": "2024-01-01T00:00:00Z"
    }
  ],
  "thinking_mode": false
}
```

**Response:**

```json
{
  "content": "I'm doing well, thank you for asking!",
  "thoughts": null,
  "timestamp": "2024-01-01T00:00:01Z"
}
```

#### Stream Message

```http
POST /api/v1/chat/messages/stream
Content-Type: application/json

{
  "message": "Tell me a story",
  "history": [],
  "thinking_mode": true
}
```

**Response (Server-Sent Events):**

```
data: {"content": "Once", "thoughts": "I should create an engaging story", "is_final": false}

data: {"content": " upon", "thoughts": "", "is_final": false}

data: {"content": " a time...", "thoughts": "", "is_final": true}
```

## 🏠 Architecture

### Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application factory
│   ├── config.py            # Configuration management
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py    # API router aggregation
│   │       └── chat.py      # Chat endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   └── database.py      # Database configuration
│   ├── models/
│   │   ├── __init__.py
│   │   └── chat.py          # SQLAlchemy models
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── chat.py          # Pydantic schemas
│   └── services/
│       ├── __init__.py
│       └── gemini.py        # Gemini AI service
├── tests/
│   ├── __init__.py
│   └── test_api.py          # API tests
├── requirements.txt
├── .env.example
├── start.sh                 # Startup script
└── README.md
```

### Core Components

#### 1. FastAPI Application (`app/main.py`)

- Application factory pattern
- CORS middleware configuration
- Lifespan management for startup/shutdown
- Automatic API documentation generation

#### 2. Configuration (`app/config.py`)

- Pydantic Settings for type-safe configuration
- Environment variable management
- Development/production configuration separation

#### 3. Gemini Service (`app/services/gemini.py`)

- Google Generative AI integration
- Streaming response support
- Thinking mode for detailed reasoning
- Error handling and retry logic

#### 4. API Endpoints (`app/api/v1/chat.py`)

- RESTful chat endpoints
- Server-Sent Events for streaming
- Comprehensive error handling
- Request/response validation

#### 5. Data Models (`app/schemas/chat.py`)

- Pydantic models for request/response validation
- Type safety and automatic documentation
- JSON serialization handling

## 🔧 Configuration

### Environment Variables

| Variable          | Description             | Default            | Required |
| ----------------- | ----------------------- | ------------------ | -------- |
| `SECRET_KEY`      | Application secret key  | -                  | ✅       |
| `DATABASE_URL`    | Database connection URL | SQLite             | ❌       |
| `GEMINI_API_KEY`  | Google Gemini API key   | -                  | ✅       |
| `GEMINI_MODEL_ID` | Gemini model identifier | `gemini-2.5-flash` | ❌       |
| `ALLOWED_ORIGINS` | CORS allowed origins    | `localhost:8080`   | ❌       |
| `DEBUG`           | Enable debug mode       | `false`            | ❌       |

### Database Configuration

#### Development (SQLite)

```bash
DATABASE_URL=sqlite:///./haxui.db
```

#### Production (PostgreSQL)

```bash
DATABASE_URL=postgresql://username:password@localhost:5432/haxui
```

## 🧪 Testing

### Run Tests

```bash
# Test dependencies are included in pyproject.toml dev dependencies
# They're installed automatically with: uv sync --dev

# Run all tests with uv
uv run pytest

# Run with coverage
uv run pytest --cov=app

# Run specific test file
uv run pytest tests/test_api.py -v
```

### Test Categories

1. **Health Check Tests** - Verify all health endpoints
2. **Chat API Tests** - Test message sending and streaming
3. **Schema Validation Tests** - Verify request/response validation
4. **Service Tests** - Test Gemini integration
5. **Error Handling Tests** - Verify error responses

## 🚀 Production Deployment

### Using Docker

1. **Build image:**

   ```bash
   docker build -t hax-ui-backend .
   ```

2. **Run container:**
   ```bash
   docker run -p 8000:8000 \
     -e SECRET_KEY=your-secret-key \
     -e GEMINI_API_KEY=your-gemini-key \
     -e DATABASE_URL=your-db-url \
     hax-ui-backend
   ```

### Using Docker Compose

```yaml
version: "3.8"
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - DATABASE_URL=postgresql://user:pass@db:5432/haxui
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=haxui
```

### Environment Considerations

- Set `DEBUG=false` in production
- Use strong `SECRET_KEY`
- Configure proper `DATABASE_URL`
- Set restrictive `ALLOWED_ORIGINS`
- Enable HTTPS in production

## 🔒 Security

### Authentication

Currently, the API doesn't implement authentication. For production use:

1. Add JWT authentication
2. Implement user management
3. Add rate limiting
4. Configure API key validation

### CORS Configuration

Configure `ALLOWED_ORIGINS` to restrict cross-origin requests:

```bash
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### API Rate Limiting

Consider implementing rate limiting for production:

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
```

## 🐛 Troubleshooting

### Common Issues

1. **Gemini API Key Error**
   - Verify `GEMINI_API_KEY` is set correctly
   - Check API key permissions and quotas

2. **Database Connection Error**
   - Verify `DATABASE_URL` format
   - Ensure database server is running
   - Check connection permissions

3. **CORS Errors**
   - Add frontend URL to `ALLOWED_ORIGINS`
   - Verify frontend is making requests to correct backend URL

4. **Port Already in Use**
   - Change port: `uvicorn app.main:app --port 8001`
   - Kill existing process: `pkill -f uvicorn`

### Debug Mode

Enable debug mode for detailed error messages:

```bash
DEBUG=true uvicorn app.main:app --reload --log-level debug
```

### Logging

Logs are output to console. For production, configure file logging:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

## 📈 Performance

### Optimization Tips

1. **Database Connection Pooling**

   ```python
   engine = create_engine(
       DATABASE_URL,
       pool_size=20,
       max_overflow=0,
       pool_pre_ping=True
   )
   ```

2. **Async Database Operations**

   ```python
   from sqlalchemy.ext.asyncio import create_async_engine
   ```

3. **Response Caching**

   ```python
   from fastapi_cache import caches
   ```

4. **Request Size Limits**
   ```python
   app.add_middleware(
       HTTPMiddleware,
       max_request_size=1024*1024  # 1MB
   )
   ```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Add tests for new functionality
4. Run tests: `uv run pytest`
5. Submit pull request

### Code Style

- Follow PEP 8
- Use type hints
- Add docstrings to functions
- Maintain test coverage above 80%

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

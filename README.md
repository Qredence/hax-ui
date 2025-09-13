# 🚀 HAX UI Registry - Advanced Chat Component Library

<div align="center">

![HAX UI Registry](https://img.shields.io/badge/HAX-UI_Registry-blue?style=for-the-badge&logo=react&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![uv](https://img.shields.io/badge/uv-DE5FE9?style=for-the-badge&logo=python&logoColor=white)

**A sophisticated chat-optimized component library with FastAPI backend and AI integration.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-20+-339933?style=for-the-badge&logo=node.js&logoColor=white)

[📖 Documentation](#-documentation) • [🧩 Components](#-components) • [🚀 Getting Started](#-getting-started) • [⚡ Features](#-features)

</div>

---

## 🌟 Overview

HAX UI Registry is an enterprise-grade component library that combines the power of **Shadcn/ui** with specialized **chat-optimized components**. Built with modern React patterns, TypeScript, and FastAPI backend, it provides a comprehensive solution for building sophisticated chat interfaces with AI integration capabilities.

### 🎯 Key Highlights

- **🔧 Dual-Registry System**: Seamlessly use both standard Shadcn/ui and HAX components
- **💬 Chat-Optimized**: Specialized components for chat interfaces with advanced features
- **🤖 AI Integration**: Built-in support for Google Gemini API with BYOK architecture
- **⚡ FastAPI Backend**: Modern async Python backend with automatic API documentation
- **🌊 Real-time Streaming**: Server-Sent Events for real-time chat responses
- **📦 uv Package Management**: Fast, modern Python dependency management
- **♿ Accessibility**: WCAG-compliant components with ARIA support
- **🔒 Security**: Built-in security scanning and vulnerability detection
- **🐳 Docker Ready**: Production-ready containerization for easy deployment

---

## 🚀 Getting Started

### Prerequisites

- **Node.js**: >= 20.0.0
- **Python**: >= 3.11
- **pnpm**: >= 10.14.0
- **uv**: Fast Python package manager
- **Git**: For version control

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Qredence/hax-ui.git
   cd hax-ui
   ```

2. **Install frontend dependencies**:
   ```bash
   pnpm install
   ```

3. **Setup backend with uv**:
   ```bash
   cd backend
   curl -LsSf https://astral.sh/uv/install.sh | sh  # Install uv if needed
   ./start.sh  # Creates .venv and starts FastAPI server
   ```

4. **Start frontend** (in another terminal):
   ```bash
   pnpm dev
   ```

5. **Access the application**:
   - Frontend: http://localhost:8080
   - Backend API Docs: http://localhost:8000/api/v1/docs
   - Health Check: http://localhost:8000/health

### Docker Deployment

```bash
# Quick start with Docker Compose
docker-compose up -d

# Access at http://localhost:8080
```

## ⚡ Features

### 🤖 AI Integration

- **Google Gemini API**: Advanced AI chat with streaming responses
- **BYOK Architecture**: Bring Your Own Key for security
- **Thought Processing**: Visualize AI reasoning process
- **Real-time Streaming**: Instant response streaming via SSE

### 🎨 Design System

- **Dual Registry**: Use both Shadcn/ui and HAX components
- **TailwindCSS**: Utility-first styling with custom design tokens
- **Consistent Variants**: Unified design language across components
- **Custom Themes**: Easy theme customization and dark mode

### 🔒 Security & Quality

- **Type Safety**: Full TypeScript frontend + Pydantic backend
- **Security Headers**: CORS, CSP, and other security measures
- **Input Validation**: Comprehensive request/response validation
- **Error Handling**: Graceful error handling and user feedback

### 🚀 Developer Experience

- **Hot Reload**: Instant development feedback
- **Component Registry**: Install components via CLI
- **API Documentation**: Automatic OpenAPI docs generation
- **Comprehensive Testing**: Vitest (frontend) + pytest (backend)

## 🧩 Components

### HAX Chat Components

#### 💬 HaxChatInput
Advanced chat input with thinking mode and auto-resize:
```tsx
import { HaxChatInput } from '@/components/hax/chat/chat-input'

<HaxChatInput
  input={input}
  onInputChange={setInput}
  onSubmit={sendMessage}
  isLoading={isLoading}
  thinkingMode={thinkingMode}
  onToggleThinking={toggleThinking}
/>
```

#### 💭 HaxChatMessage  
Rich message display with thought processing:
```tsx
import { HaxChatMessage } from '@/components/hax/chat/chat-message'

<HaxChatMessage
  message={{
    id: '1',
    content: 'Hello! How can I help?',
    role: 'assistant',
    timestamp: new Date(),
    thoughts: 'User is greeting me, I should respond warmly'
  }}
  showActions={true}
/>
```

#### 🗣️ HaxChatConversation
Full conversation interface with auto-scroll:
```tsx
import { HaxChatConversation } from '@/components/hax/chat/chat-conversation'

<HaxChatConversation
  messages={messages}
  onSendMessage={sendMessage}
  isLoading={isLoading}
/>
```

### HAX UI Components

#### 🔘 HaxButton
Chat-optimized button variants:
```tsx
import { HaxButton } from '@/components/hax/ui/button'

<HaxButton variant="chat-send" size="chat-icon">
  <ArrowUp size={16} />
</HaxButton>
```

**Variants**: `default`, `chat`, `chat-send`, `chat-thinking`
**Sizes**: `default`, `sm`, `lg`, `icon`, `chat-icon`

## 🛠️ Development

### Available Scripts

```bash
# Frontend Development
pnpm dev              # Start Vite dev server (port 8080)
pnpm build            # Production build
pnpm test             # Run Vitest tests
pnpm typecheck        # TypeScript validation

# Backend Development (uses uv)
cd backend
./start.sh            # Quick start (creates .venv automatically)
uv run pytest        # Run tests
uv sync --dev         # Install dependencies

# Full Stack
docker-compose up     # Start entire stack
```

### Project Structure

```
├── client/                    # React frontend
│   ├── components/hax/        # HAX component system
│   │   ├── ui/               # HAX UI components
│   │   ├── chat/             # Chat components
│   │   └── layout/           # Layout components
│   ├── services/             # API services
│   └── hooks/                # React hooks
├── backend/                  # FastAPI Python backend
│   ├── app/
│   │   ├── api/v1/          # API endpoints
│   │   ├── services/        # Business logic
│   │   └── schemas/         # Pydantic models
│   └── .venv/               # Local virtual environment
├── hax-registry/            # Component registry definitions
└── docs/                    # Documentation
```

## 📚 Documentation

- **[Backend API Documentation](backend/README.md)** - FastAPI setup and API reference
- **[Deployment Guide](DEPLOYMENT.md)** - Production deployment instructions
- **[Component Documentation](docs/components/)** - Detailed component guides
- **[Development Guide](docs/development.md)** - Development setup and workflows

## 🐳 Deployment

### Docker Compose (Recommended)

```bash
# Production deployment
cp .env.production .env
docker-compose up -d
```

### Manual Deployment

```bash
# Backend
cd backend
uv sync --frozen --no-dev
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000

# Frontend  
pnpm build
# Serve dist/spa/ with your web server
```

### Cloud Deployment

Supported platforms:
- **Railway** - Auto-deploy from GitHub
- **Vercel** - Frontend deployment
- **DigitalOcean** - Full stack deployment
- **AWS/Azure** - Enterprise deployment

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`  
3. Run tests: `pnpm test && cd backend && uv run pytest`
4. Commit changes: `git commit -m 'Add amazing feature'`
5. Push to branch: `git push origin feature/amazing-feature`
6. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[Shadcn/ui](https://ui.shadcn.com/)** - Incredible component system
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern Python web framework
- **[uv](https://docs.astral.sh/uv/)** - Fast Python package management
- **[TailwindCSS](https://tailwindcss.com/)** - Utility-first CSS framework
- **[Google Gemini](https://ai.google.dev/)** - Advanced AI capabilities

---

<div align="center">

**Built with ❤️ using HAX UI Registry**

[🔝 Back to top](#-hax-ui-registry---advanced-chat-component-library)

</div>
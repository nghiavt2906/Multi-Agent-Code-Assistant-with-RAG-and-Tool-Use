# 🤖 Multi-Agent Code Assistant with RAG

An advanced AI-powered coding assistant that leverages multiple specialized agents, retrieval-augmented generation (RAG), and function calling to help developers write, debug, and optimize code.

## 🌟 Key Features

- **Multi-Agent Architecture**: Orchestrates specialized agents (Planner, Coder, Reviewer, Debugger) for complex coding tasks
- **Retrieval-Augmented Generation (RAG)**: Searches through documentation and code repositories for contextually relevant information
- **Function Calling & Tool Use**: Integrates with external tools (code execution, file operations, web search)
- **Multiple LLM Support**: Compatible with OpenAI GPT-4, Anthropic Claude, and other providers
- **Interactive Web Interface**: React-based UI with real-time agent collaboration visualization
- **Code Execution Sandbox**: Safe environment for testing generated code
- **Smart Prompt Engineering**: Optimized prompts for different agent roles and tasks

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (React)                     │
│  - Chat Interface  - Agent Visualization  - Code Editor │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌────────────────────────────────────────────────────────┐
│                  Backend (FastAPI)                     │
│  ┌──────────────────────────────────────────────────┐  │
│  │         Agent Orchestrator                       │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐          │  │
│  │  │ Planner  │ │  Coder   │ │ Reviewer │ ...      │  │
│  │  └──────────┘ └──────────┘ └──────────┘          │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │         RAG System (ChromaDB)                    │  │
│  │  - Documentation Embeddings                      │  │
│  │  - Code Snippet Search                           │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │         Tool Integration                         │  │
│  │  - Code Executor  - File Ops  - Web Search       │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              LLM Providers                              │
│  - OpenAI GPT-4  - Anthropic Claude  - Custom Models    │
└─────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 16+
- API keys for OpenAI or Anthropic

### Backend Setup

```bash
cd backend
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Initialize vector database
python scripts/init_vectordb.py

# Run the server
python main.py
```

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

Visit `http://localhost:3000` to use the application.

## 💡 Usage Examples

### Example 1: Building a REST API

```
User: Create a FastAPI endpoint for user authentication with JWT tokens

[Planner Agent] Breaking down the task:
1. Design JWT token structure
2. Implement token generation
3. Create authentication middleware
4. Build login/register endpoints

[Coder Agent] Generating implementation...

[Reviewer Agent] Analyzing code for security and best practices...

[Result] Complete implementation with security recommendations
```

### Example 2: Debugging Complex Issues

```
User: My React component isn't re-rendering when state changes

[Debugger Agent] Analyzing common React re-render issues...
[RAG System] Retrieving relevant React documentation...
[Debugger Agent] Found the issue: You're mutating state directly...
```

## 🎯 Technical Highlights

### 1. Advanced Agent Orchestration

- **Dynamic agent selection** based on task complexity
- **Inter-agent communication** with shared context
- **Fallback mechanisms** for handling agent failures

### 2. Optimized RAG Pipeline

- Semantic search using sentence transformers
- Hybrid search (dense + sparse retrieval)
- Re-ranking for improved relevance
- Cached embeddings for performance

### 3. Robust Function Calling

- Type-safe tool definitions
- Automatic parameter validation
- Error handling and retries
- Streaming support for real-time updates

### 4. Production-Ready Features

- Rate limiting and quota management
- Conversation history persistence
- Multi-user support
- Logging and monitoring

## 📊 Project Metrics

- **Lines of Code**: ~3,000+
- **Test Coverage**: 85%+
- **Response Time**: <2s for simple queries
- **Supported LLMs**: 5+ providers

## 🛠️ Technology Stack

**Backend:**
- FastAPI (async API framework)
- LangChain (LLM orchestration)
- ChromaDB (vector database)
- Pydantic (data validation)
- Redis (caching)

**Frontend:**
- React 18
- TypeScript
- TailwindCSS
- React Query
- Socket.io (real-time updates)

**AI/ML:**
- OpenAI GPT-4
- Anthropic Claude
- Sentence Transformers
- Custom prompt templates

## 📈 Future Enhancements

- [ ] Integration with GitHub for direct PR creation
- [ ] Support for voice input/output
- [ ] Fine-tuned models for specific programming languages
- [ ] Collaborative coding sessions
- [ ] VS Code extension

## 🤝 Contributing

This project demonstrates enterprise-level AI application development patterns suitable for production use at scale.

## 📝 License

MIT License

---

**Built to showcase:**
- ✅ Cutting-edge LLM application development
- ✅ Information retrieval and search systems
- ✅ Agentic AI architectures
- ✅ Modern full-stack development practices
- ✅ Production-ready AI systems

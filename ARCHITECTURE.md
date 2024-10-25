# Multi-Agent Code Assistant - Architecture Diagram

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interface                          │
│                     (React + TypeScript)                        │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Chat Interface  │  Code Editor  │   Agent Visualization   │ │
│  └────────────────────────────────────────────────────────────┘ │
└───────────────────────────┬─────────────────────────────────────┘
                            │ HTTP/WebSocket
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FastAPI Backend                            │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    API Endpoints                           │ │
│  │  /chat  │  /agents  │  /tools  │  /health                  │ │
│  └──────────────────────┬─────────────────────────────────────┘ │
│                         │                                       │
│  ┌──────────────────────▼─────────────────────────────────────┐ │
│  │              Agent Orchestrator                            │ │
│  │  • Task Analysis      • Agent Selection                    │ │
│  │  • Execution Planning • Result Aggregation                 │ │
│  └──────────────────────┬─────────────────────────────────────┘ │
│                         │                                       │
│  ┌──────────────────────▼─────────────────────────────────────┐ │
│  │                  Specialized Agents                        │ │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │ │
│  │  │ Planner  │ │  Coder   │ │ Reviewer │ │ Debugger │       │ │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │ │
│  │  ┌──────────┐                                              │ │
│  │  │Optimizer │                                              │ │
│  │  └──────────┘                                              │ │
│  └──────────────────────┬─────────────────────────────────────┘ │
└─────────────────────────┼───────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  LLM Layer   │  │  RAG System  │  │ Tool System  │
├──────────────┤  ├──────────────┤  ├──────────────┤
│ • OpenAI     │  │ • ChromaDB   │  │ • Code Exec  │
│ • Anthropic  │  │ • Embeddings │  │ • File Ops   │
│ • Custom     │  │ • Search     │  │ • Web Search │
└──────────────┘  └──────────────┘  └──────────────┘
```

## Agent Workflow

```
User Query
    │
    ▼
┌─────────────────┐
│ Query Analysis  │ ─────► Identify task type
└────────┬────────┘        (code/debug/optimize)
         │
         ▼
┌─────────────────┐
│  RAG Retrieval  │ ─────► Get relevant context
└────────┬────────┘        from vector DB
         │
         ▼
┌─────────────────┐
│ Planner Agent   │ ─────► Create execution plan
└────────┬────────┘        Break down task
         │
         ▼
┌─────────────────┐
│  Coder Agent    │ ─────► Implement solution
└────────┬────────┘        Write code
         │
         ▼
┌─────────────────┐
│ Reviewer Agent  │ ─────► Check quality
└────────┬────────┘        Find issues
         │
         ▼
┌─────────────────┐
│ Response Format │ ─────► Combine results
└────────┬────────┘        Add context
         │
         ▼
    User Response
```

## Data Flow

```
┌──────────┐
│   User   │
└────┬─────┘
     │ 1. Send Message
     ▼
┌─────────────┐
│  Frontend   │
└────┬────────┘
     │ 2. POST /api/v1/chat
     ▼
┌─────────────────────────┐
│ Chat Endpoint Handler   │
└────┬────────────────────┘
     │ 3. Create Orchestrator
     ▼
┌─────────────────────────┐
│   Agent Orchestrator    │
└────┬────────────────────┘
     │
     ├─► 4a. Query RAG ─────► Vector Store
     │
     ├─► 4b. Execute Agents
     │      │
     │      ├─► Planner ──► LLM Provider
     │      ├─► Coder ────► LLM Provider
     │      └─► Reviewer ─► LLM Provider
     │
     └─► 5. Aggregate Results
         │
         ▼
     Response to User
```

## Component Responsibilities

### Frontend (React)
- **UI Components**: Chat interface, code editor, agent trace viewer
- **State Management**: Message history, loading states
- **API Client**: Axios for backend communication
- **Rendering**: Markdown + syntax highlighting

### Backend (FastAPI)
- **API Layer**: RESTful endpoints, request validation
- **Orchestration**: Agent coordination, workflow management
- **Business Logic**: Task analysis, result aggregation

### Agents
- **Planner**: Task decomposition, dependency analysis
- **Coder**: Code generation, implementation
- **Reviewer**: Code review, quality checks
- **Debugger**: Error analysis, fix suggestions
- **Optimizer**: Performance improvements

### RAG System
- **Vector Store**: Document embeddings, similarity search
- **Retrieval**: Context extraction, relevance ranking
- **Integration**: Inject context into agent prompts

### LLM Providers
- **Abstraction**: Unified interface for multiple providers
- **Error Handling**: Retries, fallbacks
- **Streaming**: Real-time token generation

### Tools
- **Code Executor**: Safe sandboxed execution
- **File Operations**: Read/write capabilities
- **Web Search**: Information retrieval

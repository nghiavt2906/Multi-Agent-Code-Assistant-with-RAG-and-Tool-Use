"""
Data models and schemas
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal
from datetime import datetime
from enum import Enum


class AgentType(str, Enum):
    """Types of agents in the system"""
    PLANNER = "planner"
    CODER = "coder"
    REVIEWER = "reviewer"
    DEBUGGER = "debugger"
    OPTIMIZER = "optimizer"


class MessageRole(str, Enum):
    """Message roles"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    AGENT = "agent"


class Message(BaseModel):
    """Chat message model"""
    role: MessageRole
    content: str
    agent_type: Optional[AgentType] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict[str, Any]] = None


class ChatRequest(BaseModel):
    """Request for chat endpoint"""
    message: str
    conversation_id: Optional[str] = None
    model: Optional[str] = None
    temperature: Optional[float] = 0.7
    use_rag: bool = True
    max_iterations: int = 5


class ChatResponse(BaseModel):
    """Response from chat endpoint"""
    response: str
    conversation_id: str
    agent_trace: List[Dict[str, Any]]
    sources: Optional[List[Dict[str, Any]]] = None
    execution_time: float


class AgentStep(BaseModel):
    """Single agent execution step"""
    agent_type: AgentType
    input: str
    output: str
    tools_used: List[str] = []
    thinking: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class CodeExecutionRequest(BaseModel):
    """Request to execute code"""
    code: str
    language: Literal["python", "javascript", "bash"] = "python"
    timeout: int = 30


class CodeExecutionResult(BaseModel):
    """Result of code execution"""
    success: bool
    output: Optional[str] = None
    error: Optional[str] = None
    execution_time: float


class DocumentChunk(BaseModel):
    """Document chunk for RAG"""
    content: str
    metadata: Dict[str, Any]
    score: Optional[float] = None


class RAGQuery(BaseModel):
    """Query for RAG system"""
    query: str
    top_k: int = 5
    filter_metadata: Optional[Dict[str, Any]] = None


class RAGResponse(BaseModel):
    """Response from RAG system"""
    results: List[DocumentChunk]
    query_time: float


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    components: Dict[str, str]

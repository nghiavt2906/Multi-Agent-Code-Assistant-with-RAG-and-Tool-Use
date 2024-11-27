"""
Chat endpoints for interacting with agents
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Optional
import uuid
from loguru import logger

from app.models import ChatRequest, ChatResponse
from app.core.orchestrator import AgentOrchestrator
from app.core.rag_system import RAGSystem
from app.core.vector_store import VectorStoreManager

router = APIRouter()

# Store active orchestrators by conversation ID
orchestrators: Dict[str, AgentOrchestrator] = {}

# Singleton RAG system instance
_rag_system: Optional[RAGSystem] = None
_rag_initialized: bool = False


async def get_rag_system() -> RAGSystem:
    """Get or create the RAG system singleton"""
    global _rag_system, _rag_initialized
    if _rag_system is None or not _rag_initialized:
        logger.info("Initializing RAG system...")
        vector_store = VectorStoreManager()
        await vector_store.initialize()
        _rag_system = RAGSystem(vector_store=vector_store)
        _rag_initialized = True
        logger.info("RAG system initialized successfully")
    return _rag_system


async def get_orchestrator(
    conversation_id: str = None,
    rag_system: RAGSystem = None
) -> AgentOrchestrator:
    """Get or create an orchestrator for a conversation"""
    if conversation_id and conversation_id in orchestrators:
        return orchestrators[conversation_id]
    
    # Create new orchestrator with RAG system
    if rag_system is None:
        rag_system = await get_rag_system()
    
    orchestrator = AgentOrchestrator(rag_system=rag_system)
    if conversation_id:
        orchestrators[conversation_id] = orchestrator
    
    return orchestrator


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint that processes user messages using multi-agent system
    
    Args:
        request: ChatRequest with user message and parameters
        
    Returns:
        ChatResponse with agent response and execution trace
    """
    try:
        # Generate conversation ID if not provided
        conversation_id = request.conversation_id or str(uuid.uuid4())
        
        logger.info(f"Processing chat request for conversation {conversation_id}")
        logger.info(f"RAG enabled: {request.use_rag}")
        
        # Get orchestrator with RAG system
        orchestrator = await get_orchestrator(conversation_id)
        
        # Execute task
        result = await orchestrator.execute_task(request)
        
        return ChatResponse(
            response=result["response"],
            conversation_id=conversation_id,
            agent_trace=result["agent_trace"],
            sources=result.get("sources"),
            execution_time=result["execution_time"]
        )
        
    except Exception as e:
        logger.error(f"Chat request failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat/reset/{conversation_id}")
async def reset_conversation(conversation_id: str):
    """Reset a conversation"""
    if conversation_id in orchestrators:
        orchestrators[conversation_id].reset()
        return {"status": "reset", "conversation_id": conversation_id}
    return {"status": "not_found", "conversation_id": conversation_id}


@router.delete("/chat/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete a conversation"""
    if conversation_id in orchestrators:
        del orchestrators[conversation_id]
        return {"status": "deleted", "conversation_id": conversation_id}
    return {"status": "not_found", "conversation_id": conversation_id}


@router.get("/chat/conversations")
async def list_conversations():
    """List active conversations"""
    return {
        "conversations": list(orchestrators.keys()),
        "count": len(orchestrators)
    }

"""
Multi-Agent Code Assistant - Main Application Entry Point
FastAPI backend for orchestrating AI agents with RAG capabilities
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
from loguru import logger
import sys

from app.config import settings
from app.api import chat, agents, tools, health
from app.core.rag_system import RAGSystem
from app.core.vector_store import VectorStoreManager

# Configure logging
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level="INFO" if not settings.DEBUG else "DEBUG"
)

# Global instances
rag_system: RAGSystem = None
vector_store: VectorStoreManager = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global rag_system, vector_store
    
    logger.info("🚀 Starting Multi-Agent Code Assistant...")
    
    # Initialize vector store
    logger.info("📊 Initializing vector database...")
    vector_store = VectorStoreManager()
    await vector_store.initialize()
    
    # Initialize RAG system
    logger.info("🧠 Initializing RAG system...")
    rag_system = RAGSystem(vector_store)
    
    logger.info("✅ Application startup complete!")
    
    yield
    
    # Cleanup
    logger.info("🔄 Shutting down application...")
    if vector_store:
        await vector_store.cleanup()
    logger.info("👋 Shutdown complete!")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Multi-Agent Code Assistant with RAG and Tool Use",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(chat.router, prefix="/api/v1", tags=["Chat"])
app.include_router(agents.router, prefix="/api/v1", tags=["Agents"])
app.include_router(tools.router, prefix="/api/v1", tags=["Tools"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Multi-Agent Code Assistant API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "status": "running"
    }


def get_rag_system() -> RAGSystem:
    """Dependency to get RAG system instance"""
    if rag_system is None:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    return rag_system


def get_vector_store() -> VectorStoreManager:
    """Dependency to get vector store instance"""
    if vector_store is None:
        raise HTTPException(status_code=503, detail="Vector store not initialized")
    return vector_store


if __name__ == "__main__":
    logger.info(f"🌐 Starting server on {settings.HOST}:{settings.PORT}")
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )

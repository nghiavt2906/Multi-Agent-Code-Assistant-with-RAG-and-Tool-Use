"""
Vector Store Manager using ChromaDB
"""

import chromadb
from chromadb.config import Settings as ChromaSettings
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Optional
from loguru import logger
import os

from app.config import settings


class VectorStoreManager:
    """Manages vector database operations"""
    
    def __init__(self):
        self.client = None
        self.collection = None
        self.embedding_model = None
        
    async def initialize(self):
        """Initialize vector store and embedding model"""
        try:
            # Create persistence directory
            os.makedirs(settings.CHROMA_PERSIST_DIR, exist_ok=True)
            
            # Initialize ChromaDB client
            self.client = chromadb.PersistentClient(
                path=settings.CHROMA_PERSIST_DIR,
                settings=ChromaSettings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name="code_docs",
                metadata={"description": "Code documentation and examples"}
            )
            
            # Load embedding model
            logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
            self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
            
            logger.info(f"Vector store initialized with {self.collection.count()} documents")
            
        except Exception as e:
            logger.error(f"Failed to initialize vector store: {e}")
            raise
    
    async def add_documents(
        self,
        documents: List[str],
        metadatas: List[Dict[str, Any]],
        ids: Optional[List[str]] = None
    ):
        """Add documents to vector store"""
        try:
            # Generate embeddings
            embeddings = self.embedding_model.encode(documents).tolist()
            
            # Generate IDs if not provided
            if ids is None:
                current_count = self.collection.count()
                ids = [f"doc_{current_count + i}" for i in range(len(documents))]
            
            # Add to collection
            self.collection.add(
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"Added {len(documents)} documents to vector store")
            
        except Exception as e:
            logger.error(f"Failed to add documents: {e}")
            raise
    
    async def search(
        self,
        query: str,
        top_k: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Search for similar documents"""
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode([query])[0].tolist()
            
            # Search
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where=filter_metadata
            )
            
            # Format results
            formatted_results = []
            if results and results['documents'] and len(results['documents']) > 0:
                for i in range(len(results['documents'][0])):
                    formatted_results.append({
                        'content': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                        'score': 1 - results['distances'][0][i] if results['distances'] else 0.0,
                        'id': results['ids'][0][i]
                    })
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []
    
    async def delete_collection(self):
        """Delete the collection"""
        try:
            self.client.delete_collection(name="code_docs")
            logger.info("Collection deleted")
        except Exception as e:
            logger.error(f"Failed to delete collection: {e}")
    
    async def cleanup(self):
        """Cleanup resources"""
        logger.info("Cleaning up vector store...")
        # ChromaDB client cleanup happens automatically

"""
RAG (Retrieval-Augmented Generation) System
"""

from typing import List, Dict, Any, Optional
from loguru import logger
import time

from app.core.vector_store import VectorStoreManager
from app.models import DocumentChunk, RAGResponse


class RAGSystem:
    """Retrieval-Augmented Generation system for code assistance"""
    
    def __init__(self, vector_store: VectorStoreManager):
        self.vector_store = vector_store
        
    async def query(
        self,
        query: str,
        top_k: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> RAGResponse:
        """
        Query the RAG system for relevant documents
        
        Args:
            query: The search query
            top_k: Number of results to return
            filter_metadata: Optional metadata filter
            
        Returns:
            RAGResponse with results and timing
        """
        start_time = time.time()
        
        try:
            # Search vector store
            results = await self.vector_store.search(
                query=query,
                top_k=top_k,
                filter_metadata=filter_metadata
            )
            
            # Convert to DocumentChunk objects
            chunks = [
                DocumentChunk(
                    content=result['content'],
                    metadata=result['metadata'],
                    score=result.get('score', 0.0)
                )
                for result in results
            ]
            
            query_time = time.time() - start_time
            
            logger.info(f"RAG query completed in {query_time:.3f}s, found {len(chunks)} results")
            
            return RAGResponse(
                results=chunks,
                query_time=query_time
            )
            
        except Exception as e:
            logger.error(f"RAG query failed: {e}")
            return RAGResponse(results=[], query_time=time.time() - start_time)
    
    async def add_documentation(
        self,
        documents: List[str],
        metadatas: List[Dict[str, Any]]
    ):
        """Add documentation to the RAG system"""
        try:
            await self.vector_store.add_documents(
                documents=documents,
                metadatas=metadatas
            )
            logger.info(f"Added {len(documents)} documents to RAG system")
        except Exception as e:
            logger.error(f"Failed to add documentation: {e}")
            raise
    
    def format_context(self, chunks: List[DocumentChunk]) -> str:
        """Format retrieved chunks into context string"""
        if not chunks:
            return ""
        
        context_parts = ["## Retrieved Context:\n"]
        for i, chunk in enumerate(chunks, 1):
            source = chunk.metadata.get('source', 'Unknown')
            context_parts.append(f"### Source {i}: {source}")
            context_parts.append(f"Relevance: {chunk.score:.2f}\n")
            context_parts.append(chunk.content)
            context_parts.append("\n---\n")
        
        return "\n".join(context_parts)

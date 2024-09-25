"""
Test vector store functionality
"""

import pytest
from app.core.vector_store import VectorStoreManager


@pytest.mark.asyncio
async def test_vector_store_initialization():
    """Test vector store can be initialized"""
    vector_store = VectorStoreManager()
    await vector_store.initialize()
    
    assert vector_store.client is not None
    assert vector_store.collection is not None
    assert vector_store.embedding_model is not None


@pytest.mark.asyncio
async def test_add_and_search_documents():
    """Test adding documents and searching"""
    vector_store = VectorStoreManager()
    await vector_store.initialize()
    
    # Add test documents
    documents = [
        "Python is a programming language",
        "JavaScript is used for web development",
        "FastAPI is a Python web framework"
    ]
    metadatas = [
        {"type": "info", "topic": "python"},
        {"type": "info", "topic": "javascript"},
        {"type": "info", "topic": "python"}
    ]
    
    await vector_store.add_documents(documents, metadatas)
    
    # Search
    results = await vector_store.search("Python web framework", top_k=2)
    
    assert len(results) > 0
    assert any("FastAPI" in r["content"] for r in results)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

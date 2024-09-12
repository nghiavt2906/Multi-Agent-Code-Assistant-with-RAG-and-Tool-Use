"""
Initialize vector database with sample documentation
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.vector_store import VectorStoreManager
from loguru import logger


SAMPLE_DOCUMENTS = [
    {
        "content": """
# FastAPI Basics

FastAPI is a modern, fast web framework for building APIs with Python 3.7+.

## Creating a Simple API

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
```

## Key Features
- Automatic API documentation
- Type hints for validation
- Async support
- Dependency injection
        """,
        "metadata": {
            "source": "FastAPI Documentation",
            "type": "tutorial",
            "language": "python"
        }
    },
    {
        "content": """
# React Hooks Guide

React Hooks let you use state and other React features without writing a class.

## useState

```javascript
import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);
  
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>
        Increment
      </button>
    </div>
  );
}
```

## useEffect

```javascript
import { useEffect } from 'react';

useEffect(() => {
  // Code to run on mount
  return () => {
    // Cleanup code
  };
}, [dependencies]);
```
        """,
        "metadata": {
            "source": "React Documentation",
            "type": "tutorial",
            "language": "javascript"
        }
    },
    {
        "content": """
# Python Error Handling Best Practices

## Try-Except Blocks

```python
try:
    result = risky_operation()
except ValueError as e:
    logger.error(f"Value error: {e}")
    result = None
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise
finally:
    cleanup()
```

## Custom Exceptions

```python
class CustomError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

raise CustomError("Something went wrong")
```
        """,
        "metadata": {
            "source": "Python Best Practices",
            "type": "guide",
            "language": "python"
        }
    },
    {
        "content": """
# Database Query Optimization

## Indexing

Create indexes on frequently queried columns:

```sql
CREATE INDEX idx_user_email ON users(email);
CREATE INDEX idx_created_at ON posts(created_at);
```

## N+1 Query Problem

Bad:
```python
# This creates N+1 queries
users = User.objects.all()
for user in users:
    print(user.profile.bio)  # Each iteration queries database
```

Good:
```python
# This uses only 2 queries
users = User.objects.select_related('profile').all()
for user in users:
    print(user.profile.bio)
```
        """,
        "metadata": {
            "source": "Database Optimization Guide",
            "type": "guide",
            "language": "sql"
        }
    },
    {
        "content": """
# Async/Await in Python

## Basic Usage

```python
import asyncio

async def fetch_data(url):
    # Simulate API call
    await asyncio.sleep(1)
    return f"Data from {url}"

async def main():
    # Run multiple tasks concurrently
    tasks = [
        fetch_data("url1"),
        fetch_data("url2"),
        fetch_data("url3")
    ]
    results = await asyncio.gather(*tasks)
    print(results)

asyncio.run(main())
```

## Error Handling in Async

```python
async def safe_fetch(url):
    try:
        return await fetch_data(url)
    except Exception as e:
        logger.error(f"Failed to fetch {url}: {e}")
        return None
```
        """,
        "metadata": {
            "source": "Python Async Guide",
            "type": "tutorial",
            "language": "python"
        }
    },
    {
        "content": """
# REST API Design Best Practices

## Endpoint Naming

- Use nouns, not verbs: `/users` not `/getUsers`
- Use plural names: `/users` not `/user`
- Use hierarchical structure: `/users/{id}/posts`

## HTTP Methods

- GET: Retrieve resources
- POST: Create new resources
- PUT: Update entire resource
- PATCH: Partial update
- DELETE: Remove resource

## Status Codes

- 200 OK: Success
- 201 Created: Resource created
- 400 Bad Request: Invalid input
- 401 Unauthorized: Authentication required
- 404 Not Found: Resource doesn't exist
- 500 Internal Server Error: Server error
        """,
        "metadata": {
            "source": "API Design Guidelines",
            "type": "guide",
            "language": "general"
        }
    }
]


async def main():
    """Initialize vector database with sample documents"""
    logger.info("Initializing vector database...")
    
    # Create vector store manager
    vector_store = VectorStoreManager()
    await vector_store.initialize()
    
    # Add sample documents
    documents = [doc["content"] for doc in SAMPLE_DOCUMENTS]
    metadatas = [doc["metadata"] for doc in SAMPLE_DOCUMENTS]
    
    logger.info(f"Adding {len(documents)} sample documents...")
    await vector_store.add_documents(documents, metadatas)
    
    logger.info("✅ Vector database initialized successfully!")
    logger.info(f"Total documents: {vector_store.collection.count()}")
    
    # Test search
    logger.info("\nTesting search functionality...")
    results = await vector_store.search("How do I handle errors in Python?", top_k=2)
    
    logger.info(f"\nFound {len(results)} results:")
    for i, result in enumerate(results, 1):
        logger.info(f"\n{i}. Score: {result['score']:.3f}")
        logger.info(f"   Source: {result['metadata'].get('source', 'Unknown')}")
        logger.info(f"   Preview: {result['content'][:100]}...")


if __name__ == "__main__":
    asyncio.run(main())

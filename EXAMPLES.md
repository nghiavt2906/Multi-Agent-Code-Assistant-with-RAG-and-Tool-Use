# Example Usage Scenarios

## 1. Building a REST API with Authentication

**User Prompt:**
```
Create a FastAPI application with user authentication using JWT tokens.
Include registration, login, and protected endpoints.
```

**Expected Response:**
- Planner Agent: Breaks down into steps (database models, JWT utilities, endpoints)
- Coder Agent: Implements complete code with FastAPI, Pydantic models, JWT handling
- Reviewer Agent: Reviews security, suggests improvements

**Sample Output:**
```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

# Configuration
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Models
class User(BaseModel):
    username: str
    email: str
    
class UserInDB(User):
    hashed_password: str

# ... (complete implementation)
```

## 2. Debugging React Component

**User Prompt:**
```
My React component won't re-render when I update state:

function Counter() {
  const [count, setCount] = useState(0);
  
  const increment = () => {
    count = count + 1; // This doesn't work!
  };
  
  return <button onClick={increment}>{count}</button>;
}
```

**Expected Response:**
- Debugger Agent: Identifies the issue (mutating state directly)
- Provides fix with explanation
- Suggests best practices

**Sample Output:**
```
🐛 Issue Identified: Direct State Mutation

Problem: You're mutating `count` directly instead of using the setter.

Fix:
```javascript
const increment = () => {
  setCount(count + 1); // Use the setter function
};
```

Or use functional update for more reliability:
```javascript
const increment = () => {
  setCount(prev => prev + 1);
};
```

## 3. Database Query Optimization

**User Prompt:**
```
Optimize this code that has N+1 query problem:

users = User.objects.all()
for user in users:
    print(user.profile.name)
    for post in user.posts.all():
        print(post.title)
```

**Expected Response:**
- Optimizer Agent: Identifies N+1 problem
- Provides optimized solution with select_related and prefetch_related
- Explains performance improvement

**Sample Output:**
```python
# Optimized version - reduces queries from N+1 to 2-3
users = User.objects.select_related('profile').prefetch_related('posts').all()

for user in users:
    print(user.profile.name)  # No additional query
    for post in user.posts.all():  # No additional queries
        print(post.title)

# Performance improvement: ~100 queries → 3 queries
```

## 4. Creating Unit Tests

**User Prompt:**
```
Write unit tests for this function:

def calculate_discount(price, discount_percent):
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Invalid discount")
    return price * (1 - discount_percent / 100)
```

**Expected Response:**
- Planner Agent: Identifies test scenarios
- Coder Agent: Writes comprehensive tests
- Reviewer Agent: Ensures edge cases are covered

**Sample Output:**
```python
import pytest

def test_calculate_discount_normal():
    assert calculate_discount(100, 10) == 90.0
    assert calculate_discount(50, 20) == 40.0

def test_calculate_discount_edge_cases():
    assert calculate_discount(100, 0) == 100.0
    assert calculate_discount(100, 100) == 0.0

def test_calculate_discount_invalid():
    with pytest.raises(ValueError):
        calculate_discount(100, -10)
    with pytest.raises(ValueError):
        calculate_discount(100, 150)

def test_calculate_discount_types():
    assert calculate_discount(100.5, 10) == 90.45
```

## 5. Implementing Async Operations

**User Prompt:**
```
Create an async function that fetches data from multiple APIs concurrently
and combines the results.
```

**Expected Response:**
- Planner Agent: Designs concurrent execution strategy
- Coder Agent: Implements with asyncio.gather
- Optimizer Agent: Suggests timeout and error handling improvements

**Sample Output:**
```python
import asyncio
import aiohttp
from typing import List, Dict, Any

async def fetch_api(session: aiohttp.ClientSession, url: str) -> Dict[str, Any]:
    """Fetch data from a single API"""
    async with session.get(url, timeout=10) as response:
        return await response.json()

async def fetch_multiple_apis(urls: List[str]) -> List[Dict[str, Any]]:
    """Fetch data from multiple APIs concurrently"""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_api(session, url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out errors
        valid_results = [r for r in results if not isinstance(r, Exception)]
        return valid_results

# Usage
urls = [
    "https://api1.example.com/data",
    "https://api2.example.com/data",
    "https://api3.example.com/data"
]

results = asyncio.run(fetch_multiple_apis(urls))
```

## 6. Code Review Request

**User Prompt:**
```
Review this code for security and best practices:

@app.post("/user/create")
def create_user(username: str, password: str):
    db.execute(f"INSERT INTO users VALUES ('{username}', '{password}')")
    return {"status": "created"}
```

**Expected Response:**
- Reviewer Agent: Identifies multiple critical issues
- Provides detailed security recommendations

**Sample Output:**
```
🔍 Critical Security Issues Found:

1. SQL Injection Vulnerability (CRITICAL)
   - Using string formatting creates SQL injection risk
   - Fix: Use parameterized queries

2. Storing Passwords in Plain Text (CRITICAL)
   - Passwords must be hashed
   - Fix: Use bcrypt or similar

3. Missing Input Validation (HIGH)
   - No validation on username/password
   - Fix: Use Pydantic models

Recommended Implementation:

from pydantic import BaseModel, constr
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])

class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=50)
    password: constr(min_length=8)

@app.post("/user/create")
async def create_user(user: UserCreate, db: Database = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    
    # Parameterized query prevents SQL injection
    await db.execute(
        "INSERT INTO users (username, password) VALUES ($1, $2)",
        user.username, hashed_password
    )
    
    return {"status": "created"}
```

## Testing These Examples

Run the backend server and try these prompts through:

1. **Web Interface**: http://localhost:3000
2. **API**: POST to http://localhost:8000/api/v1/chat
3. **Swagger UI**: http://localhost:8000/docs

Each example demonstrates different agent capabilities and showcases the multi-agent coordination.

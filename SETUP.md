# Setup Guide

## Backend Setup

### 1. Install Python Dependencies

```powershell
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```powershell
cp .env.example .env
```

Edit `.env` and add your API keys:
```
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### 3. Initialize Vector Database

```powershell
python scripts/init_vectordb.py
```

### 4. Run the Backend Server

```powershell
python main.py
```

The API will be available at `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

## Frontend Setup

### 1. Install Node Dependencies

```powershell
cd frontend
npm install
```

### 2. Run Development Server

```powershell
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Testing the Application

### Example Requests

1. **Create a REST API**
   ```
   Create a FastAPI endpoint for user authentication with JWT tokens
   ```

2. **Debug Code**
   ```
   My React component isn't re-rendering when state changes. Here's the code:
   [paste your code]
   ```

3. **Optimize Code**
   ```
   Optimize this database query to reduce N+1 queries:
   [paste your query]
   ```

### API Examples

Using cURL:

```powershell
# Health check
curl http://localhost:8000/api/v1/health

# Chat request
curl -X POST http://localhost:8000/api/v1/chat `
  -H "Content-Type: application/json" `
  -d '{
    "message": "Create a function to calculate fibonacci numbers",
    "use_rag": true,
    "temperature": 0.7
  }'

# List available agents
curl http://localhost:8000/api/v1/agents

# List available tools
curl http://localhost:8000/api/v1/tools
```

## Troubleshooting

### Backend Issues

1. **Import Errors**: Make sure all dependencies are installed
   ```powershell
   pip install -r requirements.txt
   ```

2. **Vector DB Issues**: Delete and reinitialize
   ```powershell
   rm -r data/chroma
   python scripts/init_vectordb.py
   ```

3. **API Key Errors**: Check your `.env` file

### Frontend Issues

1. **Module Not Found**: Reinstall dependencies
   ```powershell
   rm -r node_modules
   npm install
   ```

2. **Connection Errors**: Make sure backend is running on port 8000

## Production Deployment

### Backend

```powershell
# Using Gunicorn
pip install gunicorn
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend

```powershell
npm run build
# Serve the dist/ folder with your preferred static file server
```

## Environment Variables Reference

| Variable | Description | Required |
|----------|-------------|----------|
| OPENAI_API_KEY | OpenAI API key | Yes (if using GPT) |
| ANTHROPIC_API_KEY | Anthropic API key | Yes (if using Claude) |
| CHROMA_PERSIST_DIR | Vector DB storage path | No (default: ./data/chroma) |
| DEFAULT_MODEL | Default LLM model | No (default: gpt-4-turbo-preview) |
| DEFAULT_TEMPERATURE | Default temperature | No (default: 0.7) |
| DEBUG | Enable debug mode | No (default: True) |

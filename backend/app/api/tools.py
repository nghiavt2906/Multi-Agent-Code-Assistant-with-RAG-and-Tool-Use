"""
Tool execution endpoints
"""

from fastapi import APIRouter, HTTPException
from app.models import CodeExecutionRequest, CodeExecutionResult
from app.core.tools import execute_tool, AVAILABLE_TOOLS
from typing import Dict, Any

router = APIRouter()


@router.get("/tools")
async def list_tools():
    """List all available tools"""
    return {
        "tools": [
            {
                "name": tool["function"]["name"],
                "description": tool["function"]["description"],
                "parameters": tool["function"]["parameters"]
            }
            for tool in AVAILABLE_TOOLS
        ]
    }


@router.post("/tools/execute")
async def execute_tool_endpoint(tool_name: str, arguments: Dict[str, Any]):
    """Execute a tool"""
    try:
        result = await execute_tool(tool_name, arguments)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tools/code/execute", response_model=CodeExecutionResult)
async def execute_code(request: CodeExecutionRequest):
    """Execute code safely"""
    try:
        from app.core.tools import CodeExecutor
        
        executor = CodeExecutor()
        
        if request.language == "python":
            result = await executor.execute_python(request.code, request.timeout)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Language '{request.language}' not supported"
            )
        
        return CodeExecutionResult(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

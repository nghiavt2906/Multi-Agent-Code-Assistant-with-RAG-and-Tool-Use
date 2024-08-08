"""
Tools for function calling and agent actions
"""

from typing import Dict, Any
from loguru import logger
import sys
import io
from contextlib import redirect_stdout, redirect_stderr
import time


class CodeExecutor:
    """Safely execute code in a restricted environment"""
    
    @staticmethod
    async def execute_python(code: str, timeout: int = 30) -> Dict[str, Any]:
        """
        Execute Python code safely
        
        Args:
            code: Python code to execute
            timeout: Execution timeout in seconds
            
        Returns:
            Dict with success, output, and error
        """
        start_time = time.time()
        
        try:
            # Create string buffers for stdout/stderr
            stdout_buffer = io.StringIO()
            stderr_buffer = io.StringIO()
            
            # Restricted globals
            restricted_globals = {
                '__builtins__': {
                    'print': print,
                    'len': len,
                    'range': range,
                    'str': str,
                    'int': int,
                    'float': float,
                    'list': list,
                    'dict': dict,
                    'set': set,
                    'tuple': tuple,
                    'bool': bool,
                    'sum': sum,
                    'max': max,
                    'min': min,
                    'abs': abs,
                    'round': round,
                    'sorted': sorted,
                    'enumerate': enumerate,
                    'zip': zip,
                    'map': map,
                    'filter': filter,
                }
            }
            
            # Execute with timeout
            with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
                exec(code, restricted_globals, {})
            
            output = stdout_buffer.getvalue()
            error = stderr_buffer.getvalue()
            
            execution_time = time.time() - start_time
            
            return {
                "success": not error,
                "output": output,
                "error": error if error else None,
                "execution_time": execution_time
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            return {
                "success": False,
                "output": None,
                "error": str(e),
                "execution_time": execution_time
            }


class FileOperations:
    """File system operations"""
    
    @staticmethod
    async def read_file(file_path: str) -> Dict[str, Any]:
        """Read a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return {"success": True, "content": content}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def write_file(file_path: str, content: str) -> Dict[str, Any]:
        """Write to a file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}


class WebSearch:
    """Web search functionality"""
    
    @staticmethod
    async def search(query: str, max_results: int = 5) -> Dict[str, Any]:
        """
        Search the web using DuckDuckGo
        
        Args:
            query: Search query
            max_results: Maximum number of results
            
        Returns:
            Dict with search results
        """
        try:
            # Import here to handle optional dependency
            from duckduckgo_search import DDGS
            
            results = []
            with DDGS() as ddgs:
                for result in ddgs.text(query, max_results=max_results):
                    results.append({
                        "title": result.get("title", ""),
                        "url": result.get("href", ""),
                        "snippet": result.get("body", "")
                    })
            
            return {"success": True, "results": results}
            
        except ImportError:
            return {
                "success": False,
                "error": "DuckDuckGo search not available"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


# Tool definitions for function calling
AVAILABLE_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "execute_python",
            "description": "Execute Python code safely in a restricted environment",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "The Python code to execute"
                    }
                },
                "required": ["code"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results to return",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the file to read"
                    }
                },
                "required": ["file_path"]
            }
        }
    }
]


async def execute_tool(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Execute a tool by name"""
    
    executor = CodeExecutor()
    file_ops = FileOperations()
    web_search = WebSearch()
    
    if tool_name == "execute_python":
        return await executor.execute_python(arguments.get("code", ""))
    elif tool_name == "web_search":
        return await web_search.search(
            arguments.get("query", ""),
            arguments.get("max_results", 5)
        )
    elif tool_name == "read_file":
        return await file_ops.read_file(arguments.get("file_path", ""))
    else:
        return {"success": False, "error": f"Unknown tool: {tool_name}"}

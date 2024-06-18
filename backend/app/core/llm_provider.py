"""
LLM Provider Interface
Supports multiple LLM providers (OpenAI, Anthropic, etc.)
"""

from typing import List, Dict, Any, Optional, AsyncIterator
from abc import ABC, abstractmethod
from loguru import logger

from app.config import settings

try:
    from openai import AsyncOpenAI
except ImportError:
    AsyncOpenAI = None

try:
    from anthropic import AsyncAnthropic
except ImportError:
    AsyncAnthropic = None


class LLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    async def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        tools: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Generate completion"""
        pass
    
    @abstractmethod
    async def generate_stream(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> AsyncIterator[str]:
        """Generate streaming completion"""
        pass


class OpenAIProvider(LLMProvider):
    """OpenAI LLM Provider"""
    
    def __init__(self, api_key: str = None, model: str = "gpt-4-turbo-preview"):
        if AsyncOpenAI is None:
            raise ImportError("OpenAI package not installed")
        
        self.client = AsyncOpenAI(api_key=api_key or settings.OPENAI_API_KEY)
        self.model = model
    
    async def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        tools: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Generate completion using OpenAI"""
        try:
            kwargs = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            if tools:
                kwargs["tools"] = tools
                kwargs["tool_choice"] = "auto"
            
            response = await self.client.chat.completions.create(**kwargs)
            
            # Extract response
            message = response.choices[0].message
            result = {
                "content": message.content or "",
                "role": message.role,
                "finish_reason": response.choices[0].finish_reason
            }
            
            # Include tool calls if present
            if hasattr(message, 'tool_calls') and message.tool_calls:
                result["tool_calls"] = [
                    {
                        "id": tc.id,
                        "type": tc.type,
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in message.tool_calls
                ]
            
            return result
            
        except Exception as e:
            logger.error(f"OpenAI generation failed: {e}")
            raise
    
    async def generate_stream(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> AsyncIterator[str]:
        """Generate streaming completion"""
        try:
            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )
            
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            logger.error(f"OpenAI streaming failed: {e}")
            raise


class AnthropicProvider(LLMProvider):
    """Anthropic Claude Provider"""
    
    def __init__(self, api_key: str = None, model: str = "claude-3-sonnet-20240229"):
        if AsyncAnthropic is None:
            raise ImportError("Anthropic package not installed")
        
        self.client = AsyncAnthropic(api_key=api_key or settings.ANTHROPIC_API_KEY)
        self.model = model
    
    async def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        tools: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Generate completion using Anthropic"""
        try:
            # Separate system messages
            system_message = None
            chat_messages = []
            
            for msg in messages:
                if msg["role"] == "system":
                    system_message = msg["content"]
                else:
                    chat_messages.append(msg)
            
            kwargs = {
                "model": self.model,
                "messages": chat_messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            if system_message:
                kwargs["system"] = system_message
            
            if tools:
                kwargs["tools"] = tools
            
            response = await self.client.messages.create(**kwargs)
            
            # Extract content
            content = ""
            tool_calls = []
            
            for block in response.content:
                if block.type == "text":
                    content += block.text
                elif block.type == "tool_use":
                    tool_calls.append({
                        "id": block.id,
                        "type": "function",
                        "function": {
                            "name": block.name,
                            "arguments": str(block.input)
                        }
                    })
            
            result = {
                "content": content,
                "role": "assistant",
                "finish_reason": response.stop_reason
            }
            
            if tool_calls:
                result["tool_calls"] = tool_calls
            
            return result
            
        except Exception as e:
            logger.error(f"Anthropic generation failed: {e}")
            raise
    
    async def generate_stream(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> AsyncIterator[str]:
        """Generate streaming completion"""
        try:
            # Separate system messages
            system_message = None
            chat_messages = []
            
            for msg in messages:
                if msg["role"] == "system":
                    system_message = msg["content"]
                else:
                    chat_messages.append(msg)
            
            kwargs = {
                "model": self.model,
                "messages": chat_messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            if system_message:
                kwargs["system"] = system_message
            
            async with self.client.messages.stream(**kwargs) as stream:
                async for text in stream.text_stream:
                    yield text
                    
        except Exception as e:
            logger.error(f"Anthropic streaming failed: {e}")
            raise


def get_llm_provider(model: str = None) -> LLMProvider:
    """Factory function to get appropriate LLM provider"""
    model = model or settings.DEFAULT_MODEL
    
    if "gpt" in model.lower():
        return OpenAIProvider(model=model)
    elif "claude" in model.lower():
        return AnthropicProvider(model=model)
    else:
        # Default to OpenAI
        logger.warning(f"Unknown model {model}, defaulting to OpenAI")
        return OpenAIProvider(model=model)

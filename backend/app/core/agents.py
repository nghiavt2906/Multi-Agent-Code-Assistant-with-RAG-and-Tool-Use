"""
Agent Base Class and Specialized Agents
"""

from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
from loguru import logger

from app.core.llm_provider import LLMProvider, get_llm_provider
from app.models import AgentType, AgentStep


class BaseAgent(ABC):
    """Base class for all agents"""
    
    def __init__(
        self,
        agent_type: AgentType,
        llm_provider: Optional[LLMProvider] = None,
        temperature: float = 0.7
    ):
        self.agent_type = agent_type
        self.llm_provider = llm_provider or get_llm_provider()
        self.temperature = temperature
        self.conversation_history: List[Dict[str, str]] = []
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Get the system prompt for this agent"""
        pass
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """Get available tools for this agent"""
        return []
    
    async def execute(
        self,
        task: str,
        context: Optional[str] = None
    ) -> AgentStep:
        """Execute the agent's task"""
        try:
            # Build messages
            messages = [
                {"role": "system", "content": self.get_system_prompt()}
            ]
            
            # Add context if provided
            if context:
                messages.append({
                    "role": "system",
                    "content": f"Additional Context:\n{context}"
                })
            
            # Add conversation history
            messages.extend(self.conversation_history)
            
            # Add current task
            messages.append({"role": "user", "content": task})
            
            # Get tools
            tools = self.get_tools()
            
            # Generate response
            response = await self.llm_provider.generate(
                messages=messages,
                temperature=self.temperature,
                tools=tools if tools else None
            )
            
            # Extract output
            output = response.get("content", "")
            
            # Handle tool calls
            tools_used = []
            if "tool_calls" in response:
                for tool_call in response["tool_calls"]:
                    tools_used.append(tool_call["function"]["name"])
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": task})
            self.conversation_history.append({"role": "assistant", "content": output})
            
            # Create agent step
            step = AgentStep(
                agent_type=self.agent_type,
                input=task,
                output=output,
                tools_used=tools_used,
                thinking=self._extract_thinking(output)
            )
            
            logger.info(f"{self.agent_type.value} completed task")
            return step
            
        except Exception as e:
            logger.error(f"Agent {self.agent_type.value} execution failed: {e}")
            raise
    
    def _extract_thinking(self, output: str) -> Optional[str]:
        """Extract thinking/reasoning from output if present"""
        # Simple extraction - can be improved
        if "thinking:" in output.lower():
            parts = output.split("thinking:", 1)
            if len(parts) > 1:
                return parts[1].split("\n")[0].strip()
        return None
    
    def reset_history(self):
        """Reset conversation history"""
        self.conversation_history = []


class PlannerAgent(BaseAgent):
    """Agent that plans and breaks down tasks"""
    
    def __init__(self, **kwargs):
        super().__init__(agent_type=AgentType.PLANNER, **kwargs)
    
    def get_system_prompt(self) -> str:
        return """You are an expert Planning Agent specialized in breaking down complex coding tasks.

Your responsibilities:
1. Analyze the user's request and understand the full scope
2. Break down complex tasks into clear, actionable steps
3. Identify dependencies between steps
4. Determine which specialized agents (Coder, Reviewer, Debugger, Optimizer) should handle each step
5. Create a structured execution plan

Output Format:
- Provide a numbered list of steps
- For each step, specify which agent should handle it
- Include any important considerations or dependencies
- Keep the plan clear and actionable

Be thorough but concise. Focus on the logical flow of implementation."""


class CoderAgent(BaseAgent):
    """Agent that writes code"""
    
    def __init__(self, **kwargs):
        super().__init__(agent_type=AgentType.CODER, temperature=0.3, **kwargs)
    
    def get_system_prompt(self) -> str:
        return """You are an expert Coding Agent specialized in writing high-quality code.

Your responsibilities:
1. Write clean, efficient, and well-documented code
2. Follow best practices and coding standards
3. Include proper error handling
4. Add helpful comments for complex logic
5. Consider edge cases and potential issues

Guidelines:
- Use appropriate design patterns
- Write modular and reusable code
- Include type hints (Python) or types (TypeScript)
- Follow PEP 8 (Python) or standard style guides
- Provide complete implementations, not placeholders

Output your code in markdown code blocks with the appropriate language tag."""


class ReviewerAgent(BaseAgent):
    """Agent that reviews code"""
    
    def __init__(self, **kwargs):
        super().__init__(agent_type=AgentType.REVIEWER, **kwargs)
    
    def get_system_prompt(self) -> str:
        return """You are an expert Code Reviewer Agent specialized in identifying issues and improvements.

Your responsibilities:
1. Review code for correctness and bugs
2. Check for security vulnerabilities
3. Assess performance implications
4. Evaluate code quality and maintainability
5. Suggest improvements and optimizations

Review Checklist:
- Logic errors and bugs
- Security issues (SQL injection, XSS, etc.)
- Performance bottlenecks
- Code style and readability
- Error handling
- Edge cases
- Documentation quality

Output Format:
- List issues by severity (Critical, High, Medium, Low)
- Provide specific line references when possible
- Suggest concrete improvements
- Highlight what's done well"""


class DebuggerAgent(BaseAgent):
    """Agent that debugs code"""
    
    def __init__(self, **kwargs):
        super().__init__(agent_type=AgentType.DEBUGGER, **kwargs)
    
    def get_system_prompt(self) -> str:
        return """You are an expert Debugging Agent specialized in identifying and fixing code issues.

Your responsibilities:
1. Analyze error messages and stack traces
2. Identify root causes of bugs
3. Propose fixes with explanations
4. Suggest preventive measures
5. Help reproduce issues

Debugging Approach:
1. Understand the error/issue
2. Analyze the code context
3. Identify the root cause
4. Propose a fix
5. Explain why the issue occurred
6. Suggest how to prevent similar issues

Be systematic and thorough in your analysis."""


class OptimizerAgent(BaseAgent):
    """Agent that optimizes code"""
    
    def __init__(self, **kwargs):
        super().__init__(agent_type=AgentType.OPTIMIZER, **kwargs)
    
    def get_system_prompt(self) -> str:
        return """You are an expert Code Optimizer Agent specialized in improving code performance.

Your responsibilities:
1. Identify performance bottlenecks
2. Suggest algorithmic improvements
3. Optimize database queries
4. Reduce time and space complexity
5. Improve code efficiency

Optimization Areas:
- Algorithm complexity (O(n) analysis)
- Data structure selection
- Caching strategies
- Database query optimization
- Memory usage
- Parallelization opportunities

Always explain:
- What you're optimizing
- Why it's better
- Any trade-offs involved
- Expected performance improvement"""


def create_agent(agent_type: AgentType, **kwargs) -> BaseAgent:
    """Factory function to create agents"""
    agent_classes = {
        AgentType.PLANNER: PlannerAgent,
        AgentType.CODER: CoderAgent,
        AgentType.REVIEWER: ReviewerAgent,
        AgentType.DEBUGGER: DebuggerAgent,
        AgentType.OPTIMIZER: OptimizerAgent
    }
    
    agent_class = agent_classes.get(agent_type)
    if not agent_class:
        raise ValueError(f"Unknown agent type: {agent_type}")
    
    return agent_class(**kwargs)

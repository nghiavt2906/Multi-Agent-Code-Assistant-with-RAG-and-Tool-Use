"""
Agent Orchestrator - Coordinates multiple agents
"""

from typing import List, Dict, Any, Optional
from loguru import logger
import time

from app.core.agents import BaseAgent, create_agent
from app.core.rag_system import RAGSystem
from app.models import AgentType, AgentStep, ChatRequest


class AgentOrchestrator:
    """Orchestrates multiple agents to solve complex tasks"""
    
    def __init__(self, rag_system: Optional[RAGSystem] = None):
        self.rag_system = rag_system
        self.agents: Dict[AgentType, BaseAgent] = {}
        self.execution_trace: List[AgentStep] = []
    
    def get_agent(self, agent_type: AgentType) -> BaseAgent:
        """Get or create an agent"""
        if agent_type not in self.agents:
            self.agents[agent_type] = create_agent(agent_type)
        return self.agents[agent_type]
    
    async def execute_task(
        self,
        request: ChatRequest
    ) -> Dict[str, Any]:
        """
        Execute a task using multiple agents
        
        Args:
            request: Chat request with task details
            
        Returns:
            Dict with response and execution trace
        """
        start_time = time.time()
        self.execution_trace = []
        
        try:
            # Step 1: Get relevant context from RAG if enabled
            context = None
            sources = []
            
            if request.use_rag and self.rag_system:
                logger.info("Retrieving context from RAG system...")
                rag_response = await self.rag_system.query(
                    query=request.message,
                    top_k=5
                )
                
                if rag_response.results:
                    context = self.rag_system.format_context(rag_response.results)
                    sources = [
                        {
                            "content": chunk.content[:200] + "...",
                            "metadata": chunk.metadata,
                            "score": chunk.score
                        }
                        for chunk in rag_response.results
                    ]
            
            # Step 2: Plan the task
            logger.info("Planning task...")
            planner = self.get_agent(AgentType.PLANNER)
            plan_step = await planner.execute(
                task=f"Create a plan to accomplish this task:\n{request.message}",
                context=context
            )
            self.execution_trace.append(plan_step)
            
            # Step 3: Determine if we need coding
            task_lower = request.message.lower()
            needs_coding = any(keyword in task_lower for keyword in [
                "write", "code", "implement", "create", "build", "develop",
                "function", "class", "api", "endpoint"
            ])
            
            # Step 4: Execute based on task type
            if needs_coding:
                # Coding task
                coder = self.get_agent(AgentType.CODER)
                code_step = await coder.execute(
                    task=f"Implement the following:\n{request.message}\n\nPlan:\n{plan_step.output}",
                    context=context
                )
                self.execution_trace.append(code_step)
                
                # Review the code
                reviewer = self.get_agent(AgentType.REVIEWER)
                review_step = await reviewer.execute(
                    task=f"Review this code:\n{code_step.output}"
                )
                self.execution_trace.append(review_step)
                
                final_response = f"""## Implementation

{code_step.output}

## Code Review

{review_step.output}

## Execution Plan

{plan_step.output}
"""
            
            elif any(keyword in task_lower for keyword in ["debug", "fix", "error", "issue"]):
                # Debugging task
                debugger = self.get_agent(AgentType.DEBUGGER)
                debug_step = await debugger.execute(
                    task=request.message,
                    context=context
                )
                self.execution_trace.append(debug_step)
                
                final_response = f"""## Debugging Analysis

{debug_step.output}

## Initial Assessment

{plan_step.output}
"""
            
            elif any(keyword in task_lower for keyword in ["optimize", "improve", "performance"]):
                # Optimization task
                optimizer = self.get_agent(AgentType.OPTIMIZER)
                optimize_step = await optimizer.execute(
                    task=request.message,
                    context=context
                )
                self.execution_trace.append(optimize_step)
                
                final_response = f"""## Optimization Suggestions

{optimize_step.output}

## Analysis Plan

{plan_step.output}
"""
            
            else:
                # General task - just use planner + coder
                coder = self.get_agent(AgentType.CODER)
                code_step = await coder.execute(
                    task=f"{request.message}\n\nFollow this plan:\n{plan_step.output}",
                    context=context
                )
                self.execution_trace.append(code_step)
                
                final_response = f"""## Solution

{code_step.output}

## Approach

{plan_step.output}
"""
            
            execution_time = time.time() - start_time
            
            logger.info(f"Task completed in {execution_time:.2f}s using {len(self.execution_trace)} agents")
            
            return {
                "response": final_response,
                "agent_trace": [
                    {
                        "agent": step.agent_type.value,
                        "input": step.input[:200] + "..." if len(step.input) > 200 else step.input,
                        "output": step.output[:500] + "..." if len(step.output) > 500 else step.output,
                        "tools_used": step.tools_used,
                        "timestamp": step.timestamp.isoformat()
                    }
                    for step in self.execution_trace
                ],
                "sources": sources,
                "execution_time": execution_time
            }
            
        except Exception as e:
            logger.error(f"Task execution failed: {e}")
            raise
    
    def reset(self):
        """Reset all agents"""
        for agent in self.agents.values():
            agent.reset_history()
        self.execution_trace = []

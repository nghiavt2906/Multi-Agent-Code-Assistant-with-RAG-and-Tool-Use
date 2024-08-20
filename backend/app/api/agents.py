"""
Agent management endpoints
"""

from fastapi import APIRouter, HTTPException
from typing import List
from app.models import AgentType

router = APIRouter()


@router.get("/agents")
async def list_agents():
    """List all available agent types"""
    return {
        "agents": [
            {
                "type": agent_type.value,
                "description": _get_agent_description(agent_type)
            }
            for agent_type in AgentType
        ]
    }


@router.get("/agents/{agent_type}")
async def get_agent_info(agent_type: str):
    """Get information about a specific agent"""
    try:
        agent = AgentType(agent_type)
        return {
            "type": agent.value,
            "description": _get_agent_description(agent),
            "capabilities": _get_agent_capabilities(agent)
        }
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Agent type '{agent_type}' not found")


def _get_agent_description(agent_type: AgentType) -> str:
    """Get description for an agent type"""
    descriptions = {
        AgentType.PLANNER: "Plans and breaks down complex tasks into actionable steps",
        AgentType.CODER: "Writes clean, efficient code following best practices",
        AgentType.REVIEWER: "Reviews code for bugs, security issues, and improvements",
        AgentType.DEBUGGER: "Debugs code and identifies root causes of issues",
        AgentType.OPTIMIZER: "Optimizes code for better performance"
    }
    return descriptions.get(agent_type, "Unknown agent")


def _get_agent_capabilities(agent_type: AgentType) -> List[str]:
    """Get capabilities for an agent type"""
    capabilities = {
        AgentType.PLANNER: [
            "Task breakdown",
            "Dependency analysis",
            "Execution planning",
            "Agent delegation"
        ],
        AgentType.CODER: [
            "Code generation",
            "Best practices application",
            "Error handling",
            "Documentation"
        ],
        AgentType.REVIEWER: [
            "Bug detection",
            "Security analysis",
            "Code quality assessment",
            "Performance evaluation"
        ],
        AgentType.DEBUGGER: [
            "Error analysis",
            "Root cause identification",
            "Fix suggestions",
            "Prevention recommendations"
        ],
        AgentType.OPTIMIZER: [
            "Performance analysis",
            "Algorithm optimization",
            "Memory efficiency",
            "Complexity reduction"
        ]
    }
    return capabilities.get(agent_type, [])

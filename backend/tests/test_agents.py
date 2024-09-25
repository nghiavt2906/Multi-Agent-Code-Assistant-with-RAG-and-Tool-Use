"""
Simple test to verify the multi-agent system works
"""

import pytest
from app.core.agents import create_agent, AgentType
from app.models import AgentStep


@pytest.mark.asyncio
async def test_planner_agent():
    """Test planner agent execution"""
    planner = create_agent(AgentType.PLANNER)
    
    step = await planner.execute(
        task="Create a plan to build a REST API"
    )
    
    assert isinstance(step, AgentStep)
    assert step.agent_type == AgentType.PLANNER
    assert len(step.output) > 0


@pytest.mark.asyncio
async def test_coder_agent():
    """Test coder agent execution"""
    coder = create_agent(AgentType.CODER)
    
    step = await coder.execute(
        task="Write a Python function to calculate factorial"
    )
    
    assert isinstance(step, AgentStep)
    assert step.agent_type == AgentType.CODER
    assert "def" in step.output  # Should contain function definition


@pytest.mark.asyncio
async def test_agent_conversation_history():
    """Test that agents maintain conversation history"""
    agent = create_agent(AgentType.PLANNER)
    
    # First interaction
    await agent.execute(task="Hello")
    assert len(agent.conversation_history) == 2  # user + assistant
    
    # Second interaction
    await agent.execute(task="Remember what I said?")
    assert len(agent.conversation_history) == 4
    
    # Reset
    agent.reset_history()
    assert len(agent.conversation_history) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

# Contributing to Multi-Agent Code Assistant

Thank you for your interest in contributing!

## Development Setup

1. Fork the repository
2. Clone your fork
3. Install dependencies (see SETUP.md)
4. Create a feature branch

## Code Style

### Python
- Follow PEP 8
- Use type hints
- Maximum line length: 100 characters
- Use descriptive variable names

### TypeScript/React
- Use functional components with hooks
- Follow Airbnb style guide
- Use TypeScript for type safety

## Testing

### Backend Tests
```powershell
cd backend
pytest
```

### Frontend Tests
```powershell
cd frontend
npm test
```

## Pull Request Process

1. Update documentation if needed
2. Add tests for new features
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Submit PR with clear description

## Adding New Agents

To add a new agent type:

1. Update `AgentType` enum in `app/models.py`
2. Create agent class in `app/core/agents.py`
3. Add factory method in `create_agent()`
4. Update orchestrator logic if needed
5. Add tests

Example:
```python
class NewAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(agent_type=AgentType.NEW, **kwargs)
    
    def get_system_prompt(self) -> str:
        return "Your system prompt here..."
```

## Adding New Tools

To add a new tool:

1. Implement tool class in `app/core/tools.py`
2. Add tool definition to `AVAILABLE_TOOLS`
3. Update `execute_tool()` function
4. Add tests

Example:
```python
class NewTool:
    @staticmethod
    async def execute(arg: str) -> Dict[str, Any]:
        # Implementation
        return {"success": True, "result": ...}
```

## Questions?

Open an issue or reach out to maintainers.

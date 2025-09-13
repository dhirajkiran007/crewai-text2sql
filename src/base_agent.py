from crewai import Agent
from typing import Optional, List, Any

class BaseAgent(Agent):
    """Base class for all agents in the system. Extends crewai.Agent with common defaults and methods."""
    
    def __init__(
        self,
        role: str,
        goal: str,
        backstory: str,
        allow_delegation: bool = True,
        llm: Optional[str] = None,
        knowledge_sources: Optional[List[Any]] = None,
        tools: Optional[List[Any]] = None,
        **kwargs
    ):
        super().__init__(
            role=role,
            goal=goal,
            backstory=backstory,
            allow_delegation=allow_delegation,
            llm=llm,
            knowledge_sources=knowledge_sources or [],
            tools=tools or [],
            **kwargs
        )

    def perform_action(self, action: str) -> str:
        """Placeholder for common agent actions, like logging or validation."""
        return f"{self.role} performing action: {action}"

from crewai.knowledge.source.base_knowledge_source import BaseKnowledgeSource
from typing import Dict, List, Any, Optional
from pydantic import Field

class BaseCustomKnowledgeSource(BaseKnowledgeSource):
    """Base class for all custom knowledge sources in the system."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def validate_content(self, content: Dict[str, Any]) -> bool:
        """Validate loaded content before processing."""
        return bool(content)

    def format_schema(self, schema: Dict[str, List[str]]) -> Dict[str, Dict[str, List[str]]]:
        """Common formatting for database schemas."""
        return {"Database Schema": schema}

    def handle_connection_error(self, error: Exception) -> None:
        """Common error handling for connection issues."""
        raise ValueError(f"Failed to connect to data source: {str(error)}")

    def load_content(self) -> Dict[str, Any]:
        """Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement load_content method")

    def add(self) -> None:
        """Process and store the content."""
        content = self.load_content()
        if self.validate_content(content):
            self._save_documents()
        else:
            raise ValueError("Invalid content loaded from source")

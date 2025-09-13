from crewai.tools import BaseTool
from typing import Any

class BaseCustomTool(BaseTool):
    """Base class for all custom tools in the system. Extends crewai.BaseTool with common methods."""
    
    def __init__(self, name: str, description: str, **kwargs):
        super().__init__()
        self.name = name
        self.description = description

    def validate_input(self, input_data: Any) -> bool:
        """Placeholder for common input validation logic."""
        return True

    def validate_output(self, output_data: Any) -> bool:
        """Placeholder for common output validation logic."""
        return True

    def handle_error(self, error: Exception) -> dict:
        """Common error handling for all tools."""
        return {
            'status': 'error',
            'message': f"Error in {self.name}: {str(error)}",
            'data': None
        }

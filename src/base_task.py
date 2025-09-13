from crewai import Task
from typing import Optional, Any

class BaseTask(Task):
    """Base class for all tasks in the system. Extends crewai.Task with common defaults and methods."""
    
    def __init__(
        self,
        description: str,
        expected_output: str,
        agent: Any,
        **kwargs
    ):
        super().__init__(
            description=description,
            expected_output=expected_output,
            agent=agent,
            **kwargs
        )

    def validate_output(self, output: Any) -> bool:
        """Placeholder for output validation logic."""
        return True

    def preprocess_input(self, inputs: dict) -> dict:
        """Placeholder for input preprocessing."""
        return inputs

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class Environment(ABC):
    """Abstract base class for environments."""

    @abstractmethod
    def execute(self, command: str, cwd: str = "", *, timeout: Optional[int] = None) -> Dict[str, Any]:
        """Execute a command in the environment."""
        pass

    def get_template_vars(self) -> Dict[str, Any]:
        """Get template variables for this environment."""
        return {}

    def close(self):
        """Close the environment."""
        pass

    def cleanup(self):
        """Cleanup resources."""
        pass

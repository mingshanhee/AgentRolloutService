from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class Model(ABC):
    """Abstract base class for models."""
    
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def query(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Query the model with messages."""
        pass

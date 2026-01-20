from typing import Any, Dict
import logging
from runners.base import BaseRunner
try:
    from environments import get_environment
except ImportError:
    # For testing/when not running from root
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from environments import get_environment

logger = logging.getLogger(__name__)

class LocalRunner(BaseRunner):
    """Runner for local execution."""

    def __init__(self, max_resources: Dict[str, Any]):
        super().__init__(max_resources)

    def start_instance(self, instance_id: str, environment_config: Dict[str, Any]) -> str:
        """Starts a local environment instance."""
        # Check resources (simplified: assume 1 unit of 'instances' unless specified)
        needed_resources = environment_config.get("resources", {"instances": 1})
        if not self._check_resources(needed_resources):
            raise RuntimeError(f"Not enough resources. Available: {self.get_available_resources()}")

        try:
            env = get_environment(environment_config)
            # Some environments might start automatically in __init__, others might need explicit start if added
            # But based on docker.py, _start_container is called in __init__.
            self.running_instances[instance_id] = {
                "env": env,
                "resources": needed_resources
            }
            self._allocate_resources(needed_resources)
            return instance_id
        except Exception as e:
            logger.error(f"Failed to start instance {instance_id}: {e}")
            raise

    def execute_command(self, instance_id: str, cmd: str) -> Dict[str, Any]:
        """Executes a command in the local instance."""
        if instance_id not in self.running_instances:
            raise KeyError(f"Instance {instance_id} not found.")
        
        env = self.running_instances[instance_id]["env"]
        # Assuming env has an execute method as seen in docker.py
        result = env.execute(cmd)
        return result

    def close_instance(self, instance_id: str) -> None:
        """Closes the local instance."""
        if instance_id not in self.running_instances:
            return

        instance_data = self.running_instances[instance_id]
        env = instance_data["env"]
        resources = instance_data["resources"]
        
        if hasattr(env, "cleanup"):
            env.cleanup()
        elif hasattr(env, "close"):
            env.close()
            
        self._release_resources(resources)
        del self.running_instances[instance_id]

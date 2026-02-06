from typing import Any, Dict

from app.config import config


class BasicInterrupt:
    """Basic interrupt handler for dangerous operations"""

    def should_interrupt(self, state: Dict[str, Any]) -> bool:
        """Check if we should interrupt for dangerous operations"""
        if "tool_calls" in state:
            for tool_call in state["tool_calls"]:
                if tool_call.get("name") in ["delete_file", "delete_directory"]:
                    # Check if the operation is on a persistent memory path
                    arguments = tool_call.get("arguments", {})
                    if "file_path" in arguments and arguments["file_path"].startswith(
                        "/memories/"
                    ):
                        return True
                    if "directory" in arguments and arguments["directory"].startswith(
                        "/memories/"
                    ):
                        return True
                    # Always interrupt for delete operations
                    return True
        return False

    def get_interrupt_message(self, state: Dict[str, Any]) -> str:
        """Get the interrupt message for dangerous operations"""
        tool_calls = state.get("tool_calls", [])
        dangerous_operations = []

        for tool_call in tool_calls:
            tool_name = tool_call.get("name", "")
            arguments = tool_call.get("arguments", {})

            if tool_name == "delete_file":
                file_path = arguments.get("file_path", "")
                if file_path.startswith("/memories/"):
                    dangerous_operations.append(f"Delete persistent file: {file_path}")
                else:
                    dangerous_operations.append(f"Delete file: {file_path}")
            elif tool_name == "delete_directory":
                directory = arguments.get("directory", "")
                if directory.startswith("/memories/"):
                    dangerous_operations.append(
                        f"Delete persistent directory: {directory}"
                    )
                else:
                    dangerous_operations.append(f"Delete directory: {directory}")

        if dangerous_operations:
            operations_list = "\n".join([f"- {op}" for op in dangerous_operations])
            current_env = config.get_environment()
            return f"Warning: You are about to perform dangerous operations in {current_env} environment:\n{operations_list}\n\nDo you want to continue? (y/n)"

        return "Warning: You are about to perform a dangerous operation.\n\nDo you want to continue? (y/n)"

    def handle_user_response(
        self, state: Dict[str, Any], user_response: str
    ) -> Dict[str, Any]:
        """Handle user response to interrupt"""
        user_response_lower = user_response.lower().strip()

        if user_response_lower in ["y", "yes"]:
            return {"allow_operation": True, "message": "Operation approved by user"}
        else:
            return {"allow_operation": False, "message": "Operation cancelled by user"}

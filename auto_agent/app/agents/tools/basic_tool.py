"""
Basic Tool
Abstract base class for all tools
"""

import os
import subprocess
from abc import ABC, abstractmethod
from typing import Any, Dict, Literal, Optional

import requests
from langchain_core.tools import tool
from app.core.tool_registry import register_tool


class BasicTool(ABC):
    """Abstract base class for tools"""

    def __init__(self, name: str, description: str, **kwargs):
        """
        Initialize the tool

        Args:
            name: Tool name
            description: Tool description
            **kwargs: Additional parameters
        """
        self.name = name
        self.description = description
        self.kwargs = kwargs

    @abstractmethod
    def run(self, *args, **kwargs) -> Dict[str, Any]:
        """
        Run the tool

        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Tool execution result
        """
        pass

    def get_info(self) -> Dict[str, Any]:
        """
        Get tool information

        Returns:
            Tool information dictionary
        """
        return {"name": self.name, "description": self.description, **self.kwargs}

    def validate_input(self, *args, **kwargs) -> bool:
        """
        Validate input

        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Whether input is valid
        """
        # Basic validation - subclasses can override
        return True

    def execute(self, *args, **kwargs) -> Dict[str, Any]:
        """
        Execute the tool with unified error handling

        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Tool execution result with standardized format
        """
        try:
            # Validate input
            if not self.validate_input(*args, **kwargs):
                return {
                    "success": False,
                    "error": "Invalid input parameters",
                    "result": None
                }
            
            # Execute the tool
            result = self.run(*args, **kwargs)
            
            # Return standardized success response
            return {
                "success": True,
                "error": None,
                "result": result
            }
        except Exception as e:
            # Return standardized error response
            return {
                "success": False,
                "error": str(e),
                "result": None
            }


# File operation tools
@register_tool(name="list_files", description="List files in a directory")
async def list_files(directory: str = ".") -> str:
    """List files in a directory"""
    try:
        files = os.listdir(directory)
        return f"Files in {directory}: {', '.join(files)}"
    except Exception as e:
        return f"Error listing files: {str(e)}"


@register_tool(name="read_file", description="Read content of a file")
async def read_file(file_path: str) -> str:
    """Read content of a file"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except Exception as e:
        return f"Error reading file: {str(e)}"


@register_tool(name="write_file", description="Write content to a file")
async def write_file(file_path: str, content: str, overwrite: bool = False) -> str:
    """Write content to a file"""
    try:
        if os.path.exists(file_path) and not overwrite:
            return f"File {file_path} already exists. Use overwrite=True to overwrite."
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote to {file_path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"


@register_tool(name="edit_file", description="Edit content of a file")
async def edit_file(file_path: str, old_content: str, new_content: str) -> str:
    """Edit content of a file"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        new_content = content.replace(old_content, new_content)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        return f"Successfully edited {file_path}"
    except Exception as e:
        return f"Error editing file: {str(e)}"


@register_tool(name="edit_file_line", description="Edit specific line in a file")
async def edit_file_line(file_path: str, line_number: int, new_content: str) -> str:
    """Edit specific line in a file"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        if 1 <= line_number <= len(lines):
            lines[line_number - 1] = new_content + "\n"
            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(lines)
            return f"Successfully edited line {line_number} in {file_path}"
        else:
            return f"Line number {line_number} is out of range. File has {len(lines)} lines."
    except Exception as e:
        return f"Error editing file line: {str(e)}"


# Web search tool
@register_tool(name="web_search", description="Search the web for information")
async def web_search(query: str, max_results: int = 5) -> str:
    """Search the web for information"""
    try:
        # Using DuckDuckGo API as an example
        url = f"https://api.duckduckgo.com/?q={query}&format=json"
        response = requests.get(url, timeout=10)
        data = response.json()
        results = []
        if "Abstract" in data and data["Abstract"]:
            results.append(data["Abstract"])
        if "RelatedTopics" in data:
            for topic in data["RelatedTopics"][:max_results]:
                if "Text" in topic:
                    results.append(topic["Text"])
        return "\n".join(results) if results else "No results found"
    except Exception as e:
        return f"Error searching web: {str(e)}"


# Command execution tool
@register_tool(name="execute_command", description="Execute a shell command")
async def execute_command(command: str, cwd: str = ".") -> str:
    """Execute a shell command"""
    # Command whitelist for security
    ALLOWED_COMMANDS = {
        'ls', 'pwd', 'echo', 'cat', 'head', 'tail', 'wc',
        'mkdir', 'rmdir', 'cp', 'mv', 'rm',
        'git', 'python3', 'pip', 'curl', 'wget'
    }
    
    try:
        # Extract command name (first word)
        command_name = command.split()[0] if command.strip() else ''
        
        # Check if command is in whitelist
        if command_name not in ALLOWED_COMMANDS:
            return f"Error: Command '{command_name}' is not allowed. Allowed commands: {', '.join(ALLOWED_COMMANDS)}"
        
        # Validate working directory
        if not cwd or not isinstance(cwd, str):
            return "Error: Invalid working directory"
        
        # Ensure cwd is within current directory tree to prevent directory traversal
        import os
        cwd = os.path.abspath(cwd)
        current_dir = os.path.abspath('.')
        
        if not cwd.startswith(current_dir):
            return "Error: Working directory must be within the current directory tree"
        
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            cwd=cwd
        )
        output = result.stdout
        error = result.stderr
        return f"Exit code: {result.returncode}\nOutput: {output}\nError: {error}"
    except Exception as e:
        return f"Error executing command: {str(e)}"


# Python script execution tool
@register_tool(name="execute_python", description="Execute a Python script")
async def execute_python(script: str, timeout: int = 30) -> str:
    """Execute a Python script"""
    try:
        result = subprocess.run(
            ["python3", "-c", script], capture_output=True, text=True, timeout=timeout
        )
        output = result.stdout
        error = result.stderr
        return f"Exit code: {result.returncode}\nOutput: {output}\nError: {error}"
    except Exception as e:
        return f"Error executing Python script: {str(e)}"


@register_tool(name="delete_file", description="Delete a file")
async def delete_file(file_path: str) -> str:
    """Delete a file"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return f"Successfully deleted {file_path}"
        else:
            return f"File {file_path} does not exist"
    except Exception as e:
        return f"Error deleting file: {str(e)}"


@register_tool(name="delete_directory", description="Delete a directory")
async def delete_directory(directory: str) -> str:
    """Delete a directory"""
    try:
        if os.path.exists(directory):
            import shutil

            shutil.rmtree(directory)
            return f"Successfully deleted directory {directory}"
        else:
            return f"Directory {directory} does not exist"
    except Exception as e:
        return f"Error deleting directory: {str(e)}"


# Get all tools
def get_all_tools():
    """
    Get all available tools

    Returns:
        List of tools
    """
    from app.core.tool_registry import tool_registry
    return tool_registry.get_all_tools()

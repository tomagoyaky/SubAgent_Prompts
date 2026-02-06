"""
Constants
Centralized management of shared constants
"""

# API Base URLs for LLM providers
API_BASE_URLS = {
    "openai": "https://api.openai.com/v1",
    "anthropic": "https://api.anthropic.com/v1",
    "google": "https://generativelanguage.googleapis.com/v1",
    "doubao": "https://ark.cn-beijing.volces.com/api/v3",
    "glm": "https://open.bigmodel.cn/api/mcp",
    "qwen": "https://dashscope.aliyuncs.com/api/v1",
    "kimi": "https://api.moonshot.cn/v1",
    "deepseek": "https://api.deepseek.com/v1",
    "ollama": "http://localhost:11434/api",
}

# Default model names for each provider
DEFAULT_MODELS = {
    "openai": "gpt-4",
    "anthropic": "claude-3-opus-20240229",
    "google": "gemini-pro",
    "doubao": "ep-20240510182641-4l8ww",
    "glm": "glm-4",
    "qwen": "qwen-plus",
    "kimi": "moonshot-v1-8k",
    "deepseek": "deepseek-chat",
    "ollama": "llama3",
}

# Tool names
TOOL_NAMES = {
    "LIST_FILES": "list_files",
    "READ_FILE": "read_file",
    "WRITE_FILE": "write_file",
    "EDIT_FILE": "edit_file",
    "EDIT_FILE_LINE": "edit_file_line",
    "WEB_SEARCH": "web_search",
    "EXECUTE_COMMAND": "execute_command",
    "EXECUTE_PYTHON": "execute_python",
    "DELETE_FILE": "delete_file",
    "DELETE_DIRECTORY": "delete_directory",
}

# Directory types
DIRECTORY_TYPES = {
    "WORKSPACE": "workspace",
    "LOGS": "logs",
    "CONFIG": "config",
    "DATA": "data",
    "MODELS": "models",
}

# Default directory paths
DEFAULT_DIRECTORIES = {
    "workspace": "./workspace",
    "logs": "./logs",
    "config": "./config",
    "data": "./data",
    "models": "./models",
}

# LLM configuration keys
LLM_CONFIG_KEYS = {
    "DEFAULT_MODEL": "default_model",
    "TEMPERATURE": "temperature",
    "TOP_P": "top_p",
    "MAX_TOKENS": "max_tokens",
    "STREAM_MODE": "stream_mode",
    "THINKING_MODE": "thinking_mode",
}

# LLM default values
LLM_DEFAULT_VALUES = {
    "temperature": 0.7,
    "top_p": 0.9,
    "max_tokens": 2000,
    "stream_mode": False,
    "thinking_mode": False,
}

# API key environment variables
API_KEY_ENV_VARS = {
    "openai": "OPENAI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "google": "GOOGLE_API_KEY",
    "doubao": "DOUBAO_API_KEY",
    "glm": "GLM_API_KEY",
    "qwen": "QWEN_API_KEY",
    "kimi": "KIMI_API_KEY",
    "deepseek": "DEEPSEEK_API_KEY",
}

# Configuration file paths
CONFIG_FILES = {
    "YAML": "config.yaml",
    "ENV": ".env",
    "ENV_TEMPLATE": ".env.template",
}

# Log levels
LOG_LEVELS = {
    "DEBUG": "DEBUG",
    "INFO": "INFO",
    "WARNING": "WARNING",
    "ERROR": "ERROR",
    "CRITICAL": "CRITICAL",
}

# Default log level
DEFAULT_LOG_LEVEL = "INFO"

# Agent status
AGENT_STATUS = {
    "IDLE": "idle",
    "RUNNING": "running",
    "PAUSED": "paused",
    "STOPPED": "stopped",
    "ERROR": "error",
}

# Tool execution status
TOOL_STATUS = {
    "PENDING": "pending",
    "EXECUTING": "executing",
    "SUCCESS": "success",
    "FAILED": "failed",
}

# Allowed commands for execute_command tool
ALLOWED_COMMANDS = {
    'ls', 'pwd', 'echo', 'cat', 'head', 'tail', 'wc',
    'mkdir', 'rmdir', 'cp', 'mv', 'rm',
    'git', 'python3', 'pip', 'curl', 'wget'
}

# HTTP status codes
HTTP_STATUS_CODES = {
    "OK": 200,
    "BAD_REQUEST": 400,
    "UNAUTHORIZED": 401,
    "FORBIDDEN": 403,
    "NOT_FOUND": 404,
    "INTERNAL_SERVER_ERROR": 500,
}

# Timeout values (in seconds)
TIMEOUTS = {
    "HTTP_REQUEST": 30,
    "TOOL_EXECUTION": 60,
    "LLM_GENERATION": 300,
    "AGENT_STARTUP": 60,
}

# Thread pool configuration
THREAD_POOL_CONFIG = {
    "MAX_WORKERS": 10,
    "QUEUE_SIZE": 100,
}

# Regular expressions
REGEX_PATTERNS = {
    "API_KEY": r"sk-[a-zA-Z0-9]{20,}",
    "EMAIL": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+",
    "URL": r"https?://[\\w\\-]+(\\.[\\w\\-]+)+([\\w\\-.,@?^=%&:/~+#]*[\\w\\-@?^=%&/~+#])?",
}

# Error messages
ERROR_MESSAGES = {
    "LLM_INIT_FAILED": "Failed to initialize LLM provider",
    "TOOL_NOT_FOUND": "Tool not found",
    "TOOL_EXECUTION_FAILED": "Tool execution failed",
    "CONFIG_NOT_FOUND": "Configuration not found",
    "API_KEY_MISSING": "API key missing",
    "INVALID_INPUT": "Invalid input parameters",
    "DIRECTORY_NOT_FOUND": "Directory not found",
    "FILE_NOT_FOUND": "File not found",
    "PERMISSION_DENIED": "Permission denied",
    "TIMEOUT": "Operation timed out",
    "UNKNOWN_ERROR": "Unknown error",
}

# Success messages
SUCCESS_MESSAGES = {
    "LLM_INIT_SUCCESS": "LLM provider initialized successfully",
    "TOOL_EXECUTION_SUCCESS": "Tool executed successfully",
    "CONFIG_LOADED": "Configuration loaded successfully",
    "AGENT_STARTED": "Agent started successfully",
    "AGENT_STOPPED": "Agent stopped successfully",
    "FILE_CREATED": "File created successfully",
    "FILE_UPDATED": "File updated successfully",
    "DIRECTORY_CREATED": "Directory created successfully",
}

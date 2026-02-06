# Auto Agent

Auto Agent is an intelligent agent system based on LangChain, LangGraph, and DeepAgents frameworks. It consists of a master agent that decomposes tasks and distributes them to sub-agents for execution.

## Features

- **LLM Support**: Supports multiple large language models including DeepSeek-Chat, Ollama, GLM, Qwen, Doubao, Kimi, MiniPro, GPT, and Claude
- **Agent Architecture**: Master-agent and sub-agent architecture for task decomposition and execution
- **Stream Mode**: Supports both generate and stream output modes
- **Thinking Mode**: Supports thinking mode for more thoughtful responses
- **Extensible**: Modular design with abstract base classes for easy extension

## Project Structure

```
auto_agent/
  ├── app/
  │   ├── llms/           # LLM providers
  │   ├── agents/         # Agent implementations
  │   ├── utils/          # Utility functions
  │   ├── config.py       # Configuration management
  │   └── main.py         # Main application
  ├── .env                # Environment variables
  ├── .env.template       # Environment variables template
  ├── config.yaml         # Configuration file
  ├── start.sh            # Startup script
  ├── run.py              # Run script
  ├── requirements.txt    # Dependencies
  └── README.md           # This file
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd auto_agent
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.template .env
   # Edit .env file with your API keys
   ```

## Usage

### Run with startup script
```bash
chmod +x start.sh
./start.sh
```

### Run directly
```bash
python run.py
```

## Configuration

### Environment Variables
- `DEEPSEEK_API_KEY`: API key for DeepSeek
- `GLM_API_KEY`: API key for GLM
- `QWEN_API_KEY`: API key for Qwen
- `DOUBAO_API_KEY`: API key for Doubao
- `KIMI_API_KEY`: API key for Kimi
- `MINIPRO_API_KEY`: API key for MiniPro
- `GPT_API_KEY`: API key for GPT
- `CLAUDE_API_KEY`: API key for Claude

### Configuration File
Edit `config.yaml` to adjust system settings including:
- LLM parameters (temperature, top_p, max_tokens)
- Agent settings
- Directory paths
- Log levels

## Supported Models

- Ollama (local)
- DeepSeek-Chat
- GLM
- Qwen
- Doubao
- Kimi
- MiniPro
- GPT
- Claude

## License

MIT License

from langchain.agents.middleware import AgentMiddleware

from app.agents.tools.basic_tool import get_all_tools


class BasicMiddleware(AgentMiddleware):
    tools = get_all_tools()

import os

from dotenv import load_dotenv
from google.adk import Agent
from google.adk.tools import MCPToolset
from google.adk.tools import VertexAiSearchTool
from google.adk.tools.mcp_tool import StreamableHTTPConnectionParams

from WorkshopAgent.subagents.search_agent import search_agent
from WorkshopAgent.utils import get_gcloud_access_token


load_dotenv()

def get_mcp_tools():
    url = os.environ["MCP_URL"]
    print('url', url)
    return MCPToolset(
        connection_params=StreamableHTTPConnectionParams(
            url=url,
            # headers={"Authorization": f"Bearer {get_gcloud_access_token()}"}
        )
    )


mcp_agent= Agent(
    model="gemini-2.5-flash",
    name="WeatherAgent",
    description="Agent to troubleshoot different IT systems.",
    instruction=(
        "You are a helpful and friendly assistant. "
        "Your main task is to support users in diagnosing and troubleshooting errors in IT systems. "
        "You are equipped with specialized tools to perform diagnoses and to search a knowledge base containing manuals and guides for various situations. "
        "Provide clear, actionable, and understandable recommendations based on the information you find."
        "Whenever you are asked to get details about certain errors redirect to the search_agent."
    ),
    before_model_callback=[],
    after_model_callback=[],
    before_agent_callback=[],
    after_agent_callback=[],
    sub_agents=[search_agent],
    tools=[ get_mcp_tools()],

)
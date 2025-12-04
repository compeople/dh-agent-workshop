import asyncio
import os

import nest_asyncio
from dotenv import load_dotenv
from google.adk import Agent
from google.adk.tools import AgentTool
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams

from WorkshopAgent.subagents.search_agent import search_agent

load_dotenv()


def get_mcp_tools() -> McpToolset:
    url = os.environ["MCP_URL"]
    print({'MCP': url})
    return McpToolset(
        connection_params=StreamableHTTPServerParams(
            url=url,
        ),
        # this is needed according to here https://github.com/google/adk-python/issues/1024#issuecomment-2943058567
        errlog=None
    )


project_id = os.environ['GOOGLE_CLOUD_PROJECT']
datastore_id = os.environ['DATASTORE_ID']
datastore_location = f"projects/{project_id}/locations/eu/collections/default_collection/dataStores/{datastore_id}"


async def setup_agent():
    tools = []
    mcp_tools = get_mcp_tools()

    tools.append(AgentTool(agent=search_agent))
    tools.append(mcp_tools)

    return Agent(
        model="gemini-2.5-flash",
        name="ITAgent",
        description="Agent to troubleshoot different IT systems.",
        instruction=(
            "You are a helpful and friendly assistant. Whenever a user asks about troubleshooting, error messages, or IT problems, you must use the TroubleshootingAgent tool to answer the request. "
            "The TroubleshootingAgent tool is specialized in searching the knowledge base for manuals, guides, and troubleshooting tips. "
            "Always use the TroubleshootingAgent tool for any queries related to errors, issues, or troubleshooting in IT systems. "
            "Never answer troubleshooting questions yourself; always use the TroubleshootingAgent tool."
        ),
        before_model_callback=[],
        after_model_callback=[],
        before_agent_callback=[],
        after_agent_callback=[],
        sub_agents=[],
        tools=tools,
    )


nest_asyncio.apply()
root_agent = asyncio.run(setup_agent())

import os

from dotenv import load_dotenv
from google.adk import Agent
from google.adk.tools import MCPToolset
from google.adk.tools import VertexAiSearchTool
from google.adk.tools.mcp_tool import StreamableHTTPConnectionParams

from WorkshopAgent.utils import get_gcloud_access_token

project_id = os.environ['GOOGLE_CLOUD_PROJECT']
datastore_id = os.environ['DATASTORE_ID']
DATASTORE_PATH = f"projects/{project_id}/locations/eu/collections/default_collection/dataStores/{datastore_id}"

vertex_search_tool = VertexAiSearchTool(data_store_id=DATASTORE_PATH, bypass_multi_tools_limit=True)


search_agent = Agent(
    model="gemini-2.5-flash",
    name="TroubleshootingAgent",
    instruction=f"""You are a helpful assistant that answers questions based on information found in the document store: {DATASTORE_PATH}.
       Use the search tool to find relevant information before answering.
       If the answer isn't in the documents, say that you couldn't find the information.
       """,
    description="Answers questions using a specific Vertex AI Search datastore.",
    before_model_callback=[],
    after_model_callback=[],
    before_agent_callback=[],
    after_agent_callback=[],
    sub_agents=[],
    tools=[vertex_search_tool],

)
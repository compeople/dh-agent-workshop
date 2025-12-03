## Uncomment the following line/# s to deploy the agent
import json
import logging
import os
import subprocess

import requests
import vertexai
from vertexai import agent_engines
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from WorkshopAgent.agent import root_agent
from dotenv import load_dotenv

load_dotenv()

# Add the parent directory to the path so WorkshopAgent can be imported

logger = logging.getLogger(__name__)


def get_gcloud_access_token():
    try:
        token = (
            subprocess.check_output(["gcloud", "auth", "print-access-token"])
            .strip()
            .decode("utf-8")
        )
        return token
    except subprocess.CalledProcessError as e:
        logger.error(
            f"Error getting gcloud access token: {e}",
        )
        return None


def create_agent(project_id, agentspace_app_id, reasoning_engine, agent_name):
    # Get the access token
    access_token = get_gcloud_access_token()
    if not access_token:
        return

    # Define the API endpoint URL
    url = f"https://eu-discoveryengine.googleapis.com/v1alpha/projects/{project_id}/locations/eu/collections/default_collection/engines/{agentspace_app_id}/assistants/default_assistant/agents/"

    # Define the request headers
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Goog-User-Project": project_id,
    }

    # Define the JSON payload as a Python dictionary
    payload = {
        "displayName": agent_name,
        "description": "Agent to process preliminary risk inquiries and provide a list of possible companies.",
        "adk_agent_definition": {
            "tool_settings": {
                "tool_description": "Agent to process preliminary risk inquiries and provide a list of possible companies, based on the given diagnosis information."
            },
            "provisioned_reasoning_engine": {"reasoning_engine": reasoning_engine},
            "authorizations": [],
        },
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    response.raise_for_status()
    logger.info("Agent created successfully")


def deploy_agent():

    project_id = os.environ['GOOGLE_CLOUD_PROJECT']
    location = os.environ['GOOGLE_CLOUD_LOCATION']
    staging_bucket = os.environ['STAGING_BUCKET']
    agent_name = os.getenv("AGENT_NAME", "Workshop_Agent").replace(" ", "_")
    agent_description = os.getenv("AGENT_DESCRIPTION", "")
    reasoning_engine = os.getenv("REASONING_ENGINE", None)
    gemini_enterprise_app_id = os.getenv("GEMINI_ENTERPRISE_APP_ID", None)

    logger.info("Deploy to")

    logger.info(f"{project_id} {location} {staging_bucket}")
    logger.info(f"{agent_name} {agent_description} {reasoning_engine} {gemini_enterprise_app_id}")
    logger.info(f"reasoning engine: {reasoning_engine}")
    vertexai.init(
        project=project_id,
        location=location,
        staging_bucket=staging_bucket,
    )
    os_keys = ["DATASTORE_ID", "MCP_URL"]
    if not reasoning_engine:
        # deploy to agent engine
        logger.info("Deploying to Agent Engine...")
        remote_app = agent_engines.create(
            agent_engine=root_agent,  # type: ignore
            requirements="WorkshopAgent/requirements.txt",
            extra_packages=["WorkshopAgent"],
            display_name=agent_name,
            description=agent_description,
            env_vars=os_keys,
        )
        reasoning_engine = remote_app.gca_resource.name

        if gemini_enterprise_app_id is not None:
            logger.info('Deploying to Gemini Enterprise')
            create_agent(
                project_id=project_id,
                agentspace_app_id=gemini_enterprise_app_id,
                reasoning_engine=reasoning_engine,
                agent_name=agent_name,
            )
        else:
            logger.info("Gemini Enterprise App ID not given, cannot deploy to GE.")
    else:
        agent_engines.update(
            resource_name=reasoning_engine,
            agent_engine=root_agent,  # type: ignore
            requirements="WorkshopAgent/requirements.txt",
            extra_packages=["WorkshopAgent"],
            display_name=agent_name,
            description=agent_description,
            env_vars=os_keys,
        )


if __name__ == "__main__":
    deploy_agent()

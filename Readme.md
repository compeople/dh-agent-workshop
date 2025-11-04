# Overview
This repo contains an example ADK Agent with deployment script and additionally an example mcp server. 
# ADK Example
## Set up

### Create and activate your virtual environment

It is recommended to use **Python 3.12** to create your virtual environment.

```bash
python -m venv .venv
```

```bash
source .venv/bin/activate
```

### Dependency Management

install dependencies using

```
pip install -r WeatherAgent/requirements.txt
```

### Environment variables

Before running the project, create an .env file inside the app directory.

From the root directory, run the following command to create the file:

```bash
cd src && cat <<EOF > .env
GOOGLE_CLOUD_PROJECT={google_cloud_project}
GOOGLE_GENAI_USE_VERTEXAI=true
GOOGLE_CLOUD_LOCATION={location}
STAGING_BUCKET={staging_bucket}
AGENT_NAME={agent_name}
AGENT_DESCRIPTION={agent_description}
GEMINI_ENTERPRISE_APP_ID={gemini_enterprise_app_id}
EOF
```

## Run the project
### Default login for local testing

configure the right project
```bash
gcloud config set project {google_cloud_project}
```

login
```bash
gcloud auth login --update-adc
```

### Local Development
To start the web interface and test agents, navigate to the app directory and run:
```
adk web
```
## Deployment
There is a deployment script to deploy to AgentEngine in deployment/

### Creating a new Agent in Agent Engine
To create a new Agent in AgentEngine, make sure you have **NOT** set the REASONING_AGENT variable in your environment.
If you want to register the created Agent to Gemini Enterprise, make sure you set the GEMINI_ENTERPRISE_APP_ID. 
Then simply run the deployment/deploy_agent.py from your root directory.
```bash
python deployment/deploy_agent.py
```
The script shows the created reasoning agent as output, store the value in the REASONING_AGENT env variable. 
When you now run the deployment script it will update the existing agent instead of creating a new one.

### Update an existing Agent
Make sure you set the REASONING_AGENT env var with the value of your reasoning engine:
```bash
export REASONING_AGENT="projects/{project_id}/locations/{location}/reasoningEngines/{agent_id}"
```
or better add it to your .env file.

Then simply run the deployment/deploy_agent.py from your root directory.
```bash
python deployment/deploy_agent.py
```

# MCP Server
## Setup

### Dependency Management
This folder uses poetry for dependency management.
```bash
pip install poetry
```

Install dependencies using poetry:
```bash
poetry install
```

## Run the project
To run the MCP Server just run the main.py
```bash
python main.py
```

## Deployment
The MCP Server can be deployed to cloud run, using
```bash
gcloud run deploy mcp-server --no-allow-unauthenticated --region={region} --source .
```
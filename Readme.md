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

#!/bin/bash
source ../.env
echo "Deploying to Project: $GOOGLE_CLOUD_PROJECT  Region: $GOOGLE_CLOUD_LOCATION Staging Bucket: $STAGING_BUCKET"
adk deploy agent_engine --project=$GOOGLE_CLOUD_PROJECT --region=$GOOGLE_CLOUD_LOCATION --staging_bucket=$STAGING_BUCKET ../WeatherAgent
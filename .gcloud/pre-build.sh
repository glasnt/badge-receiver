#!/bin/bash
shopt -s expand_aliases

source util.sh

export BUCKET=${PROJECT_ID}-media

gcloud config set project $PROJECT_ID
gcloud config set run/platform managed
gcloud config set run/region $REGION

stepdo "Creating dedicated service account for $SERVICE_NAME"
gcloud iam service-accounts create $SERVICE_NAME \
  --display-name "$SERVICE_NAME service account"
quiet gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member serviceAccount:$SA_EMAIL \
    --role roles/run.admin
stepdone

stepdo "Create Storage bucket"
gsutil mb -l ${REGION} gs://${BUCKET}
gsutil iam ch serviceAccount:${SA_EMAIL}:roles/storage.objectAdmin gs://${BUCKET}
stepdone

echo "Pre-build provisioning complete ✨"

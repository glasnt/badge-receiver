#!/bin/bash
shopt -s expand_aliases

stepdo() { echo "→ ${1}..." }
function quiet { $* > /dev/null }

export BUCKET=${GOOGLE_CLOUD_PROJECT}-media
export SA_EMAIL=${K_SERVICE}@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com

gcloud config set project $GOOGLE_CLOUD_PROJECT
gcloud config set run/platform managed
gcloud config set run/region $GOOGLE_CLOUD_REGION

stepdo "Creating dedicated service account for $K_SERVICE"
gcloud iam service-accounts create $K_SERVICE \
  --display-name "$K_SERVICE service account"
quiet gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
    --member serviceAccount:$SA_EMAIL \
    --role roles/run.admin
stepdone

stepdo "Create Storage bucket"
gsutil mb -l ${GOOGLE_CLOUD_REGION} gs://${BUCKET}
gsutil iam ch serviceAccount:${SA_EMAIL}:roles/storage.objectAdmin gs://${BUCKET}
stepdone

echo "Pre-build provisioning complete ✨"

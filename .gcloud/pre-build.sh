#!/bin/bash
shopt -s expand_aliases

stepdo() { 
    echo "→ ${1}..." 
}

function quiet { 
    $* > /dev/null
}

stepdone(){
    statuscode=$?
    msg="... done"
    if [ $statuscode -ne 0 ]; then msg="❌  done, but non-zero return code ($statuscode)"; fi
    echo $msg
    echo " "
}

export BUCKET=${GOOGLE_CLOUD_PROJECT}-media
export SA_EMAIL=${K_SERVICE}@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com

echo "🚀 Running pre-build provisioning steps for deploying $K_SERVICE to $GOOGLE_CLOUD_PROJECT in $GOOGLE_CLOUD_REGION"

gcloud config set project $GOOGLE_CLOUD_PROJECT
gcloud config set run/platform managed
gcloud config set run/region $GOOGLE_CLOUD_REGION

stepdo "Enable additional Google Cloud APIs"
gcloud services enable cloudbuild.googleapis.com
stepdone

stepdo "Creating dedicated service account for $K_SERVICE"
gcloud iam service-accounts create $K_SERVICE \
  --display-name "$K_SERVICE service account"
quiet gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
    --member serviceAccount:$SA_EMAIL \
    --role roles/run.admin
stepdone

stepdo "Create Storage bucket"
gsutil mb -l ${GOOGLE_CLOUD_REGION} gs://${BUCKET}
stepdone

stepdo "Grant service account admin access on Storage bucket"
gsutil iam ch serviceAccount:${SA_EMAIL}:roles/storage.objectAdmin gs://${BUCKET}
stepdone

echo "Pre-build provisioning complete ✨"

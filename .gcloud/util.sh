#!/bin/bash
stepdo() {
    echo "→ ${1}..."
}

function quiet {
    $* > /dev/null
}


export PROJECT_ID=$GOOGLE_CLOUD_PROJECT
export REGION=$GOOGLE_CLOUD_REGION
export SERVICE_NAME=$K_SERVICE

export BUCKET=${PROJECT_ID}-media
export SA_EMAIL=${SERVICE_NAME}@${PROJECT_ID}.iam.gserviceaccount.com

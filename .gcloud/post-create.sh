#!/bin/bash
shopt -s expand_aliases

stepdo() { echo "→ ${1}..." }

export SA_EMAIL=${K_SERVICE}@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com
export SERVICE_URL=$(gcloud run services describe $K_SERVICE --format "value(status.url)")

stepdo "Assigning service account to service"
gcloud run services update $K_SERVICE \
    --service_account $SA_EMAIL
stepdone

echo "ℹ️  Use the following file for your cloud-build-notifier config.yaml: "
echo ""
sed -e "s/\${SERVICE_URL}/${SERVICE_URL}/" ../config.yaml
echo ""

echo "Post-create configuration complete ✨"



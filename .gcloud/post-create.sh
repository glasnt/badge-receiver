#!/bin/bash
shopt -s expand_aliases

source util.sh
export SERVICE_URL=$(gcloud run services describe $SERVICE --format "value(status.url)")

stepdo "Assigning service account to service"
gcloud run services update $SERVICE \
    --service_account $SA_EMAIL
stepdone

echo "ℹ️  Use the following file for your cloud-build-notifier config.yaml: "
echo ""
sed -e "s/\${SERVICE_URL}/${SERVICE_URL}/" ../config.yaml
echo ""

echo "Post-create configuration complete ✨"



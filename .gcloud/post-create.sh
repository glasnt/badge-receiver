#!/bin/bash
shopt -s expand_aliases

stepdo() { 
    echo "→ ${1}..." 
}

stepdone(){
    statuscode=$?
    msg="... done"
    if [ $statuscode -ne 0 ]; then msg="❌  done, but non-zero return code ($statuscode)"; fi
    echo $msg; echo " "
}

export SA_EMAIL=${K_SERVICE}@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com
export SERVICE_URL=$(gcloud run services describe $K_SERVICE --format "value(status.url)")

stepdo "Assigning service account to service"
gcloud run services update $K_SERVICE \
    --service-account $SA_EMAIL 
stepdone

echo "ℹ️  Use the following file for your cloud-build-notifier config.yaml: "
echo ""
sed -e "s|SERVICE_URL|${SERVICE_URL}|" ../config.yaml
echo ""

echo "Post-create configuration complete ✨"



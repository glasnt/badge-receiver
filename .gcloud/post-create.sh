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

sed -e "s|SERVICE_URL|${SERVICE_URL}|" config-template.yaml > config.yaml

stepdo "Retrieving latest cloud-build-notifiers setup script"
curl https://raw.githubusercontent.com/GoogleCloudPlatform/cloud-build-notifiers/master/setup.sh -o setup.sh
chmod +x setup.sh
stepdone

stepdo "Running cloud-build-notifiers setup script"
./setup.sh http config.yaml
stepdone

echo "Post-create configuration complete ✨"

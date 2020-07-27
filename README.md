# Badge Receiver

[![Status badge](https://badge-receiver-ewtifq52za-uc.a.run.app/badge/badge-receiver.svg)](https://badge-receiver-ewtifq52za-uc.a.run.app/badges)

Designed to be the receiver for a HTTP [cloud-build-notifier](https://github.com/GoogleCloudPlatform/cloud-build-notifiers), this services takes whatever information it can from a Cloud Build success or failure message and creates a badge in a specified storage container for later retrieval.


## Deployment

[![Run on Google Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run)

This will: 
 
 * create a Google Cloud Storage bucket for badge images
 * deploy this badge-reciver service
 * create a `config.yaml` that uses the deployed service, based on the `config-template.yaml`
 * run the latest version of the [cloud-build-notifier `./setup.sh` script](https://github.com/GoogleCloudPlatform/cloud-build-notifiers/blob/master/setup.sh)

## Functionality

For any Cloud Build job that is run on the project in which this project is deployed, a number of badges will be created: 

 * Any tags from the cloudbuild.yaml
 * Any substitutions from the declared list (see `SUBS` variable)

The badge will be created from the output of [shields.io](https://shields.io/#your-badge): 

 * **Label**: The tag, or substitutions value, 
 * **Message**: the short commit sha,
 * **Success Color**: Green on success, Red on fail. 

Sheild.io sample image: ![badge sample](https://img.shields.io/badge/label-message-brightgreen)

Badge images are then available at: 

 * `/service/${_SERVICE}.svg`
 * `/tag/${TAG}.svg`

For example: given the `cloudbuild.yaml` file in this repo, the following images are updated when this service is deployed: 

 * `/service/badge-receiver.svg` (![https://badge-receiver-ewtifq52za-uc.a.run.app/service/badge-receiver.svg])
 * `/tag/badge-receiver.svg` (![https://badge-receiver-ewtifq52za-uc.a.run.app/tag/badge-receiver.svg])


### Admin

Navigating to `/badges` will show all the current badges in the storage bucket, including the last updated relative time.


## Local testing

See helper commands in `Makefile`

## Notes

* Disclaimer: This is not an officially supported Google product.
* See LICENSE for the licensing information.

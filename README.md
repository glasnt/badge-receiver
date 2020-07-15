# Badge Receiver

![Status badge](https://badge-receiver-ul5eoxp2iq-uc.a.run.app/badge/badge-receiver.svg)

Designed to be the receiver for a HTTP [cloud-build-notifier](https://github.com/GoogleCloudPlatform/cloud-build-notifiers). 


## Deployment

[![Run on Google Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run)

This will: 
 
 * create a Google Cloud Storage bucket for badge images
 * deploy this badge-reciver service
 * create a `config.yaml` that uses the deployed service, based on the `config-template.yaml`
 * run the latest version of the [cloud-build-notifier `./setup.sh` script](https://github.com/GoogleCloudPlatform/cloud-build-notifiers/blob/master/setup.sh)

## Functionality

TODO: document use

## Local testing

See helper commands in `Makefile`

## Notes

* Disclaimer: This is not an officially supported Google product.
* See LICENSE for the licensing information.

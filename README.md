# Badge Receiver

Designed to be the receiver for a HTTP [cloud-build-notifier](https://github.com/GoogleCloudPlatform/cloud-build-notifiers). 

## Deployment

[![Run on Google Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run)

In the provided template `config.yaml`, replace `SERVICE_URL` with your new service. 

Then,  run cloud-build-notifier's [`./setup.sh`](https://github.com/GoogleCloudPlatform/cloud-build-notifiers#setup-script) with this config: 

```
./setup.sh http path/to/config.yaml
```

## Local testing

See helper commands in `Makefile`

## Notes

* Disclaimer: This is not an officially supported Google product.
* See LICENSE for the licensing information.

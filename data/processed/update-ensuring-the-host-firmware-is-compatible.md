# Ensuring the host firmware is compatible with the update

You are responsible for the firmware versions that you run in your clusters.
Updating host firmware is not a part of the OpenShift Container Platform update process.
It is not recommended to update firmware in conjunction with the OpenShift Container Platform version.

> **IMPORTANT:** Hardware vendors advise that it is best to apply the latest certified firmware version for the specific hardware that you are running. For each different use case, always verify firmware updates in test environments before applying them in production. For example, workloads with high throughput requirements can be negatively affected outdated host firmware. You should thoroughly test new firmware updates to ensure that they work as expected with the current version of OpenShift Container Platform. For best results, test the latest firmware version with the target OpenShift Container Platform update version.
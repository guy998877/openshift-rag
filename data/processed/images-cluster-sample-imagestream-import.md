# Configuring periodic importing of Cluster Sample Operator image stream tags

You can ensure that you always have access to the latest versions of the Cluster Sample Operator images by periodically importing the image stream tags when new versions become available.

.Procedure

1. Fetch all the imagestreams in the `openshift` namespace by running the following command:
```bash
oc get imagestreams -n openshift
```

1. Fetch the tags for every imagestream in the `openshift` namespace by running the following command:
```bash
$ oc get is <image-stream-name> -o jsonpath="{range .spec.tags[*]}{.name}{'\t'}{.from.name}{'\n'}{end}" -n openshift
```
For example:
```bash
$ oc get is ubi8-openjdk-17 -o jsonpath="{range .spec.tags[*]}{.name}{'\t'}{.from.name}{'\n'}{end}" -n openshift
```
.Example output
```bash
1.11	registry.access.redhat.com/ubi8/openjdk-17:1.11
1.12	registry.access.redhat.com/ubi8/openjdk-17:1.12
```

1. Schedule periodic importing of images for each tag present in the image stream by running the following command:
```bash
$ oc tag <repository/image> <image-stream-name:tag> --scheduled -n openshift
```
For example:
```bash
$ oc tag registry.access.redhat.com/ubi8/openjdk-17:1.11 ubi8-openjdk-17:1.11 --scheduled -n openshift
```
```bash
$ oc tag registry.access.redhat.com/ubi8/openjdk-17:1.12 ubi8-openjdk-17:1.12 --scheduled -n openshift
```
> **NOTE:** Using the `--scheduled` flag is recommended to periodically re-import an image when working with an external container image registry. The `--scheduled` flag helps to ensure that you receive the latest versions and security updates. Additionally, this setting allows the import process to automatically retry if a temporary error initially prevents the image from being imported. By default, scheduled image imports occur every 15 minutes cluster-wide.

1. Verify the scheduling status of the periodic import by running the following command:
```bash
oc get imagestream <image-stream-name> -o jsonpath="{range .spec.tags[*]}Tag: {.name}{'\t'}Scheduled: {.importPolicy.scheduled}{'\n'}{end}" -n openshift
```
For example:
```bash
oc get imagestream ubi8-openjdk-17 -o jsonpath="{range .spec.tags[*]}Tag: {.name}{'\t'}Scheduled: {.importPolicy.scheduled}{'\n'}{end}" -n openshift
```
.Example output
```bash
Tag: 1.11	Scheduled: true
Tag: 1.12	Scheduled: true
```
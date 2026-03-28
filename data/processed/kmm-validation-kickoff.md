# Validation kickoff

Preflight validation is triggered by creating a `PreflightValidationOCP` resource in the cluster. This resource contains the following fields:

`dtkImage`:: The DTK container image released for the specific OpenShift Container Platform version of the cluster. If this value is not set, the `DTK_AUTO` feature cannot be used.
You can obtain the image by running one of the following commands in the cluster:
```bash
# For x86_64 image:
$ oc adm release info quay.io/openshift-release-dev/ocp-release:4.21.0-x86_64 --image-for=driver-toolkit
```
```bash
# For ARM64 image:
$ oc adm release info quay.io/openshift-release-dev/ocp-release:4.21.0-aarch64 --image-for=driver-toolkit
```

`kernelVersion`:: Required field that provides the version of the kernel that the cluster is upgraded to.
You can obtain the version by running the following command in the cluster:
```bash
$ podman run -it --rm $(oc adm release info quay.io/openshift-release-dev/ocp-release:4.21.0-x86_64 --image-for=driver-toolkit) cat /etc/driver-toolkit-release.json
```

`pushBuiltImage`:: If `true`, then the images created during the Build and Sign validation are pushed to their repositories. This field is `false` by default.
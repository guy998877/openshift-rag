# Preparing your cluster to gather support data

Clusters using a restricted network must import the default must-gather image to gather debugging data for Red Hat support. The must-gather image is not imported by default, and clusters on a restricted network do not have access to the internet to pull the latest image from a remote repository.

.Procedure

1. If you have not added your mirror registry's trusted CA to your cluster's image configuration object as part of the Cluster Samples Operator configuration, perform the following steps:
.. Create the cluster's image configuration object:
```bash
$ oc create configmap registry-config --from-file=${MIRROR_ADDR_HOSTNAME}..5000=$path/ca.crt -n openshift-config
```

.. Add the required trusted CAs for the mirror in the cluster's image
configuration object:
```bash
$ oc patch image.config.openshift.io/cluster --patch '{"spec":{"additionalTrustedCA":{"name":"registry-config"}}}' --type=merge
```

1. Import the default must-gather image from your installation payload:
```bash
$ oc import-image is/must-gather -n openshift
```

When running the `oc adm must-gather` command, use the `--image` flag and point to the payload image, as in the following example:
```bash
$ oc adm must-gather --image=$(oc adm release info --image-for must-gather)
```
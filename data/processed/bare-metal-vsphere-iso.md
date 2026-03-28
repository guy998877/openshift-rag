# Creating RHCOS machines using an ISO image

To add bare-metal compute machines to your VMware vSphere cluster, you must manually provision them using an RHCOS ISO image and the `coreos-installer` utility.

:FeatureName: Bare-metal nodes on vSphere clusters

.Prerequisites

- You have access to the RHCOS ISO image that matches your cluster version.
- You have an HTTP server accessible to the bare-metal machine to host the Ignition config file.
- You have disabled the vSphere CSI driver.
- The OpenShift CLI (`oc`) is installed.

.Procedure

1. Extract the Ignition config file for the worker node type from the cluster by running the following command:
```bash
$ oc extract -n openshift-machine-api secret/worker-user-data-managed --keys=userData --to=- > worker.ign
```

1. Upload the `worker.ign` Ignition config file to your HTTP server. Record the URL of this file.

1. Validate that the Ignition file is accessible from the network. The following example uses `curl` to verify the file presence:
```bash
$ curl -I http://<http_server>/worker.ign
```

1. Boot the bare-metal machine using the RHCOS ISO image.

1. From the installation console, run the `coreos-installer` command:
```bash
$ sudo coreos-installer install /dev/sda \
    --ignition-url=http://<http_server>/worker.ign \
    --insecure-ignition \
    --platform=none
```
where:
`/dev/sda`:: Specifies the target install device for your hardware.
`<http_server>`:: Specifies the address of your web server.

1. Reboot the machine:
```bash
$ reboot
```

1. Monitor the boot process. After the machine reboots, it attempts to join the cluster and generates certificate signing requests (CSRs).

.Verification

- Verify that the new compute machine has joined the cluster and is in the `Ready` state:
```bash
$ oc get nodes
```
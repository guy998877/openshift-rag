# Configuring a private storage endpoint on Azure by enabling the Image Registry Operator to discover VNet and subnet names

The following procedure shows you how to set up a private storage endpoint on Azure by configuring the Image Registry Operator to discover VNet and subnet names.

.Prerequisites

- You have configured the image registry to run on Azure.
- Your network has been set up using the Installer Provisioned Infrastructure installation method.
For users with a custom network setup, see "Configuring a private storage endpoint on Azure with user-provided VNet and subnet names".

.Procedure

1. Edit the Image Registry Operator `config` object and set `networkAccess.type` to `Internal`:
```bash
$ oc edit configs.imageregistry/cluster
```
```bash
# ...
spec:
  # ...
   storage:
      azure:
        # ...
        networkAccess:
          type: Internal
# ...
```

1. Optional: Enter the following command to confirm that the Operator has completed provisioning. This might take a few minutes.
```bash
$ oc get configs.imageregistry/cluster -o=jsonpath="{.spec.storage.azure.privateEndpointName}" -w
```

1. Optional: If the registry is exposed by a route, and you are configuring your storage account to be private, you must disable redirect if you want pulls external to the cluster to continue to work. Enter the following command to disable redirect on the Image Operator configuration:
```bash
$ oc patch configs.imageregistry cluster --type=merge -p '{"spec":{"disableRedirect": true}}'
```
> **NOTE:** When redirect is enabled,  pulling images from outside of the cluster will not work.

.Verification

1. Fetch the registry service name by running the following command:
```bash
$ oc get imagestream -n openshift
```
.Example output
```bash
NAME   IMAGE REPOSITORY                                                 TAGS     UPDATED
cli    image-registry.openshift-image-registry.svc:5000/openshift/cli   latest   8 hours ago
...
```

1. Enter debug mode by running the following command:
```bash
$ oc debug node/<node_name>
```

1. Run the suggested `chroot` command. For example:
```bash
$ chroot /host
```

1. Enter the following command to log in to your container registry:
```bash
$ podman login --tls-verify=false -u unused -p $(oc whoami -t) image-registry.openshift-image-registry.svc:5000
```
.Example output
```bash
Login Succeeded!
```

1. Enter the following command to verify that you can pull an image from the registry:
```bash
$ podman pull --tls-verify=false image-registry.openshift-image-registry.svc:5000/openshift/tools
```
.Example output
```bash
Trying to pull image-registry.openshift-image-registry.svc:5000/openshift/tools/openshift/tools...
Getting image source signatures
Copying blob 6b245f040973 done
Copying config 22667f5368 done
Writing manifest to image destination
Storing signatures
22667f53682a2920948d19c7133ab1c9c3f745805c14125859d20cede07f11f9
```
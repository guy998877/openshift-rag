# Rebuilding SQLite database catalog images

You can rebuild your SQLite database catalog image with the latest version of the `opm` CLI tool that is released with your version of OpenShift Container Platform.

.Prerequisites

- You have a SQLite database catalog source.
- You have access to the cluster as a user with the `cluster-admin` role.
- You have the latest version of the `opm` CLI tool released with OpenShift Container Platform 
4.21 
on your workstation.

.Procedure

- Run the following command to rebuild your catalog with a more recent version of the `opm` CLI tool:
```bash
$ opm index add --binary-image \
  registry.redhat.io/openshift4/ose-operator-registry-rhel9:v4.21 \
  --from-index <your_registry_image> \
  --bundles "" -t \<your_registry_image>
```
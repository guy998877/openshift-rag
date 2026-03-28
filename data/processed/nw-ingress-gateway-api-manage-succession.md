# Preparing for Gateway API management succession by the Ingress Operator

Starting in OpenShift Container Platform 4.19, the Ingress Operator manages the lifecycle of any Gateway API custom resource definitions (CRDs). This means that you will be denied access to creating, updating, and deleting any CRDs within the API groups that are grouped under Gateway API.

Updating from a version before 4.19 of OpenShift Container Platform where this management was not present requires you to replace or remove any Gateway API CRDs that already exist in the cluster so that they conform to the specific OpenShift Container Platform specification required by the Ingress Operator. OpenShift Container Platform version 4.19 requires Gateway API Standard version 1.2.1 CRDs.

> **WARNING:** Updating or deleting Gateway API resources can result in downtime and loss of service or data. Be sure you understand how this will affect your cluster before performing the steps in this procedure. If necessary, back up any Gateway API objects in YAML format in order to restore it later.

.Prerequisites
- You have installed the OpenShift CLI (`oc`).
- You have access to an OpenShift Container Platform account with cluster administrator access.
- Optional: You have backed up any necessary Gateway API objects.
> **WARNING:** Backup and restore can fail or result in data loss for any CRD fields that were present in the old definitions but are absent in the new definitions.

.Procedure

1. List all the Gateway API CRDs that you need to remove by running the following command:
```bash
$ oc get crd | grep -F -e gateway.networking.k8s.io -e gateway.networking.x-k8s.io
```
.Example output
```bash
gatewayclasses.gateway.networking.k8s.io
gateways.gateway.networking.k8s.io
grpcroutes.gateway.networking.k8s.io
httproutes.gateway.networking.k8s.io
referencegrants.gateway.networking.k8s.io
```

1. Delete the Gateway API CRDs from the previous step by running the following command:
```bash
$ oc delete crd gatewayclasses.networking.k8s.io && \
oc delete crd gateways.networking.k8s.io && \
oc delete crd grpcroutes.gateway.networking.k8s.io && \
oc delete crd httproutes.gateway.networking.k8s.io && \
oc delete crd referencesgrants.gateway.networking.k8s.io
```
> **IMPORTANT:** Deleting CRDs removes every custom resource that relies on them and can result in data loss. Back up any necessary data before deleting the Gateway API CRDs. Any controller that was previously managing the lifecycle of the Gateway API CRDs will fail to operate properly. Attempting to force its use in conjunction with the Ingress Operator to manage Gateway API CRDs might prevent the cluster update from succeeding.

1. Get the supported Gateway API CRDs by running the following command:
```bash
$ oc apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.2.1/standard-install.yaml
```
> **WARNING:** You can perform this step without deleting your CRDs. If your update to a CRD removes a field that is used by a custom resource, you can lose data. Updating a CRD a second time, to a version that re-adds a field, can cause any previously deleted data to reappear. Any third-party controller that depends on a specific Gateway API CRD version that is not supported in OpenShift Container Platform 4.21 will break upon updating that CRD to one supported by Red Hat. For more information on the OpenShift Container Platform implementation and the dead fields issue, see _Gateway API implementation for OpenShift Container Platform_.
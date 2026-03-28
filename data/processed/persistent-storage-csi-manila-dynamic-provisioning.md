# Dynamically provisioning Manila CSI volumes

OpenShift Container Platform installs a storage class for each available Manila share type.

The YAML files that are created are completely decoupled from Manila and from its Container Storage Interface (CSI) plugin. As an application developer, you can dynamically provision ReadWriteMany (RWX) storage and deploy pods with applications that safely consume the storage using YAML manifests.

You can use the same pod and persistent volume claim (PVC) definitions on-premise that you use with OpenShift Container Platform on AWS, Google Cloud, Azure, and other platforms, with the exception of the storage class reference in the PVC definition.

> **IMPORTANT:** By default, the access rule that is assigned to a volume is `0.0.0.0/0`, which allows access from all IPv4 clients. To limit client access, create custom storage classes that use specific client IP addresses or subnets. For more information, see Section _Customizing Manila share access rules_.

> **NOTE:** Manila service is optional. If the service is not enabled in Red Hat OpenStack Platform (RHOSP), the Manila CSI driver is not installed and the storage classes for Manila are not created.

.Prerequisites

- RHOSP is deployed with appropriate Manila share infrastructure so that it can be used to dynamically provision and mount volumes in OpenShift Container Platform.

.Procedure (UI)

To dynamically create a Manila CSI volume using the web console:

1. In the OpenShift Container Platform console, click *Storage* → *Persistent Volume Claims*.

1. In the persistent volume claims overview, click *Create Persistent Volume Claim*.

1. Define the required options on the resulting page.

.. Select the appropriate storage class.

.. Enter a unique name for the storage claim.

.. Select the access mode to specify read and write access for the PVC you are creating.
> **IMPORTANT:** Use RWX if you want the PV that fulfills this PVC to be mounted to multiple pods on multiple nodes in the cluster.

1. Define the size of the storage claim.

1. Click *Create* to create the PVC and generate a PV.

.Procedure (CLI)

To dynamically create a Manila CSI volume using the command-line interface (CLI):

1. Create and save a file with the `PersistentVolumeClaim` object described by the following YAML:

.pvc-manila.yaml
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-manila
spec:
  accessModes: <1>
    - ReadWriteMany
  resources:
    requests:
      storage: 10Gi
  storageClassName: csi-manila-gold <2>
```
<1> Use RWX if you want the PV that fulfills this PVC to be mounted to multiple pods on multiple nodes in the cluster.
<2> The name of the storage class that provisions the storage back end. Manila storage classes are provisioned by the Operator and have the `csi-manila-` prefix.

1. Create the object you saved in the previous step by running the following command:
```bash
$ oc create -f pvc-manila.yaml
```
A new PVC is created.

1. To verify that the volume was created and is ready, run the following command:
```bash
$ oc get pvc pvc-manila
```
The `pvc-manila` shows that it is `Bound`.

You can now use the new PVC to configure a pod.
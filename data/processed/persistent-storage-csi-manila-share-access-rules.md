# Customizing Manila share access rules

By default, OpenShift Container Platform creates Manila storage classes that provide access to all IPv4 clients. To limit client access, you can define custom storage classes that use specific client IP addresses or subnets by using the `nfs-ShareClient` parameter.

> **IMPORTANT:** When using custom storage classes with restricted access rules, ensure that: * The specified IP addresses or subnets include all OpenShift Container Platform nodes that need to access the storage. * The Manila service in RHOSP supports the share type specified in the storage class. * Network connectivity exists between the allowed clients and the Manila share servers.

.Prerequisites

- Red Hat OpenStack Platform (RHOSP) is deployed with appropriate Manila share infrastructure.
- Access to a cluster with administrator privileges.

.Procedure

1. Create a YAML file for your custom storage class based on the following example:
.Example custom storage class file
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: csi-manila-gold-restricted <1>
provisioner: manila.csi.openstack.org
parameters:
  type: gold <2>
  nfs-ShareClient: "10.0.0.0/24,192.168.1.100" <3>
  csi.storage.k8s.io/provisioner-secret-name: manila-csi-secret
  csi.storage.k8s.io/provisioner-secret-namespace: openshift-manila-csi-driver
  csi.storage.k8s.io/controller-expand-secret-name: manila-csi-secret
  csi.storage.k8s.io/controller-expand-secret-namespace: openshift-manila-csi-driver
  csi.storage.k8s.io/node-stage-secret-name: manila-csi-secret
  csi.storage.k8s.io/node-stage-secret-namespace: openshift-manila-csi-driver
  csi.storage.k8s.io/node-publish-secret-name: manila-csi-secret
  csi.storage.k8s.io/node-publish-secret-namespace: openshift-manila-csi-driver
allowVolumeExpansion: true
```
<1> Descriptive name for your custom storage class.
<2> The Manila share type. This type must match an existing share type in your RHOSP environment.
<3> Comma-separated list of IP addresses or CIDR subnets allowed to access the NFS shares. The `nfs-ShareClient` parameter accepts various formats:
- Single IP address: `192.168.1.100`
- CIDR subnet: `10.0.0.0/24`
- Multiple entries: `10.0.0.0/24,192.168.1.100,172.16.0.0/16`
Ensure that the specified IP addresses or subnets include the OpenShift Container Platform cluster nodes to allow proper mounting of the persistent volumes.
In this example, access is restricted to the `10.0.0.0/24` subnet, and the specific IP address is `192.168.1.100`.

1. Apply the storage class from the file by running the following command:
```bash
$ oc apply -f custom-manila-storageclass.yaml
```

1. Verify that the storage class was created by running the following command:
```bash
$ oc get storageclass csi-manila-gold-restricted
```
.Example output
```bash
NAME                 		    PROVISIONER                RECLAIMPOLICY   VOLUMEBINDINGMODE   ALLOWVOLUMEEXPANSION   AGE
csi-manila-gold-restricted	manila.csi.openstack.org   Delete          Immediate           true                   43m
```

1. Create a persistent volume claim (PVC) that uses the custom storage class based on the following example:
.Example PVC file
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-manila-restricted
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 10Gi
  storageClassName: csi-manila-gold-restricted <1>
```
<1> The name of your custom storage class that has restricted access. In this example, the name is `csi-manila-gold-restricted`.

1. Apply the PVC from the file by running the following command:
```bash
$ oc apply -f pvc-manila-restricted.yaml
```
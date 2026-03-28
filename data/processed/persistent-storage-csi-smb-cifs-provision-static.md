# Static provisioning

You can use static provisioning to create a persistent volume (PV) and persistent volume claim (PVC) to consume existing Server Message Block protocol (SMB) shares:

.Prerequisites
- Access to the OpenShift Container Platform web console.
- {FeatureName} CSI Driver Operator and driver installed.
- You have installed the SMB server and know the following information about the server:
- Hostname
- Share name
- Username and password

.Procedure

To set up static provisioning:

1. Create a Secret for access to the Samba server using the following command with the following example YAML file:
```bash
--
$ oc create -f <file_name>.yaml
--
+
[source,yaml]
.Secret example YAML file
--
apiVersion: v1
kind: Secret
metadata:
  name: smbcreds <1>
  namespace: samba-server <2>
stringData:
  username: <username> <3>
  password: <password> <4>
--
<1> Name of the Secret for the Samba server.
<2> Namespace for the Secret for the Samba server.
<3> Username for the Secret for the Samba server.
<4> Password for the Secret for the Samba server.

. Create a PV by running the following command with the following example YAML file:
+
[source,terminal]
```
$ oc create -f <pv_file_name>.yaml <1>
<1> The name of the PV YAML file.
.Example PV YAML file
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  annotations:
    pv.kubernetes.io/provisioned-by: smb.csi.k8s.io
  name: <pv_name> <1>
spec:
  capacity:
    storage: 100Gi
  accessModes:
    - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain
  storageClassName: ""
  mountOptions:
    - dir_mode=0777
    - file_mode=0777
  csi:
    driver: smb.csi.k8s.io
    volumeHandle: smb-server.default.svc.cluster.local/share## <2>
    volumeAttributes:
      source: //<hostname>/<shares> <3>
    nodeStageSecretRef:
      name: <secret_name_shares> <4>
      namespace: <namespace> <5>
```
<1> The name of the PV.
<2> `volumeHandle` format: {smb-server-address}#{sub-dir-name}#{share-name}. Ensure that this value is unique for every share in the cluster.
<3> The Samba server must be installed somewhere and reachable from the cluster with <hostname> being the hostname for the Samba server and <shares> the path the server is configured to have among the exported shares.
<4> The name of the Secret for the shares.
<5> The applicable namespace.

1. Create a PVC:

.. Create a PVC by running the following command with the following example YAML file:
```bash
$ oc create -f <pv_file_name>.yaml <1>
```
<1> The name of the PVC YAML file.
.Example PVC YAML file
```yaml
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: <pvc_name> <1>
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: <storage_amount> <2>
  storageClassName: ""
  volumeName: <pv_name> <3>
```
<1> The name of the PVC.
<2> Storage request amount.
<3> The name of the PV from the first step.

.. Ensure that the PVC was created and is in the "Bound" status by running the following command:
```bash
$ oc describe pvc <pvc_name> <1>
```
<1> The name of the PVC that you created in the preceding step.
.Example output
```bash
Name:          pvc-test
Namespace:     default
StorageClass:  
Status:        Bound <1>
...
```
<1> PVC is in Bound status.

1. Create a deployment on Linux by running the following command with the following example YAML file:
> **NOTE:** The following deployment is not mandatory for using the PV and PVC created in the previous steps. It is example of how they can be used.
```bash
$ oc create -f <deployment_file_name>.yaml <1>
```
<1> The name of the deployment YAML file.
.Example deployment YAML file
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: nginx
  name: <deployment_name> <1>
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
      name: <deployment_name> <1>
    spec:
      nodeSelector:
        "kubernetes.io/os": linux
      containers:
        - name: <deployment_name> <1>
          image: quay.io/centos/centos:stream8
          command:
            - "/bin/bash"
            - "-c"
            - set -euo pipefail; while true; do echo $(date) >> <mount_path>/outfile; sleep 1; done <2>
          volumeMounts:
            - name: <vol_mount_name> <3>
              mountPath: <mount_path> <2>
              readOnly: false
      volumes:
        - name: <vol_mount_name> <3>
          persistentVolumeClaim:
            claimName: <pvc_name> <4>
  strategy:
    rollingUpdate:
      maxSurge: 0
      maxUnavailable: 1
    type: RollingUpdate
```
<1> The name of the deployment.
<2> The volume mount path.
<3> The name of the volume mount.
<4> The name of the PVC created in the preceding step.

1. Check the setup by running the `df -h` command in the container:
```bash
$ oc exec -it <pod_name> -- df -h <1>
```
<1> The name of the pod.
.Example output
```bash
Filesystem            Size  Used Avail Use% Mounted on
...
/dev/sda1              97G   21G   77G  22% /etc/hosts
//20.43.191.64/share   97G   21G   77G  22% /mnt/smb
...
```
In this example, there is a `/mnt/smb` directory mounted as a Common Internet File System (CIFS) filesystem.
# Provisioning a CSI volume clone

When you create a cloned persistent volume claim (PVC) API object, you trigger the provisioning of a CSI volume clone. The clone pre-populates with the contents of another PVC, adhering to the same rules as any other persistent volume. The one exception is that you must add a `dataSource` that references an existing PVC in the same namespace.

.Prerequisites
- You are logged in to a running OpenShift Container Platform cluster.
- Your PVC is created using a CSI driver that supports volume cloning.
- Your storage back end is configured for dynamic provisioning. Cloning support is not available for static provisioners.

.Procedure

To clone a PVC from an existing PVC:

1. Create and save a file with the `PersistentVolumeClaim` object described by the following YAML:

.pvc-clone.yaml
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-1-clone
  namespace: mynamespace
spec:
  storageClassName: csi-cloning <1>
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
  dataSource:
    kind: PersistentVolumeClaim
    name: pvc-1
```
<1> The name of the storage class that provisions the storage back end. The default storage class can be used and `storageClassName` can be omitted in the spec.
1. Create the object you saved in the previous step by running the following command:
```bash
$ oc create -f pvc-clone.yaml
```
A new PVC `pvc-1-clone` is created.

1. Verify that the volume clone was created and is ready by running the following command:
```bash
$ oc get pvc pvc-1-clone
```
The `pvc-1-clone` shows that it is `Bound`.
You are now ready to use the newly cloned PVC to configure a pod.

1. Create and save a file with the `Pod` object described by the YAML. For example:

```yaml
kind: Pod
apiVersion: v1
metadata:
  name: mypod
spec:
  containers:
    - name: myfrontend
      image: dockerfile/nginx
      volumeMounts:
      - mountPath: "/var/www/html"
        name: mypd
  volumes:
    - name: mypd
      persistentVolumeClaim:
        claimName: pvc-1-clone <1>
```
<1> The cloned PVC created during the CSI volume cloning operation.
The created `Pod` object is now ready to consume, clone, snapshot, or delete your cloned PVC independently of its original `dataSource` PVC.
# Attach the local claim

After a local volume has been mapped to a persistent volume claim
it can be specified inside of a resource.

.Prerequisites

- A persistent volume claim exists in the same namespace.

.Procedure

1. Include the defined claim in the resource spec. The following example
declares the persistent volume claim inside a pod:
```yaml
apiVersion: v1
kind: Pod
spec:
# ...
  containers:
    volumeMounts:
    - name: local-disks <1>
      mountPath: /data <2>
  volumes:
  - name: local-disks
    persistentVolumeClaim:
      claimName: local-pvc-name <3>
# ...
```
<1> The name of the volume to mount.
<2> The path inside the pod where the volume is mounted. Do not mount to the container root, `/`, or any path that is the same in the host and the container. This can corrupt your host system if the container is sufficiently privileged, such as the host `/dev/pts` files. It is safe to mount the host by using `/host`.
<3> The name of the existing persistent volume claim to use.

1. Create the resource in the OpenShift Container Platform cluster, specifying the file
you just created:
```bash
$ oc create -f <local-pod>.yaml
```
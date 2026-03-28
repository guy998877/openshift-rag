# Encrypting container persistent volumes on AWS with a KMS key

Defining a KMS key to encrypt container-persistent volumes on AWS is useful when you have explicit compliance and security guidelines when deploying to AWS.

.Prerequisites

- Underlying infrastructure must contain storage.
- You must create a customer KMS key on AWS.

.Procedure

1. Create a storage class:
```yaml
$ cat << EOF | oc create -f -
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: <storage-class-name> <1>
parameters:
  fsType: ext4 <2>
  encrypted: "true"
  kmsKeyId: keyvalue <3>
provisioner: ebs.csi.aws.com
reclaimPolicy: Delete
volumeBindingMode: WaitForFirstConsumer
EOF
```
<1> Specifies the name of the storage class.
<2> File system that is created on provisioned volumes.
<3> Specifies the full Amazon Resource Name (ARN) of the key to use when encrypting the container-persistent volume. If you do not provide any key, but the `encrypted` field is set to `true`, then the default KMS key is used. See [Finding the key ID and key ARN on AWS](https://docs.aws.amazon.com/kms/latest/developerguide/find-cmk-id-arn.html) in the AWS documentation.

1. Create a persistent volume claim (PVC) with the storage class specifying the KMS key:
```yaml
$ cat << EOF | oc create -f -
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mypvc
spec:
  accessModes:
    - ReadWriteOnce
  volumeMode: Filesystem
  storageClassName: <storage-class-name>
  resources:
    requests:
      storage: 1Gi
EOF
```

1. Create workload containers to consume the PVC:
```yaml
$ cat << EOF | oc create -f -
kind: Pod
metadata:
  name: mypod
spec:
  containers:
    - name: httpd
      image: quay.io/centos7/httpd-24-centos7
      ports:
        - containerPort: 80
      volumeMounts:
        - mountPath: /mnt/storage
          name: data
  volumes:
    - name: data
      persistentVolumeClaim:
        claimName: mypvc
EOF
```
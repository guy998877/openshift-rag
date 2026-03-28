# Benchmarking Kopia hashing, encryption, and splitter algorithms

Run Kopia commands to benchmark the hashing, encryption, and splitter algorithms. Based on the benchmarking results, you can select the most suitable algorithm for your workload. You run the Kopia benchmarking commands from a pod on the cluster. The benchmarking results can vary depending on CPU speed, available RAM, disk speed, current I/O load, and so on.

.Prerequisites

- You have installed the OADP Operator.
- You have an application with persistent volumes running in a separate namespace.
- You have run a backup of the application with Container Storage Interface (CSI) snapshots.

.Procedure

1. Configure the `must-gather` pod as shown in the following example. Make sure you are using the `oadp-mustgather` image for OADP version 1.3 and later.
.Example pod configuration

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: oadp-mustgather-pod
  labels:
    purpose: user-interaction
spec:
  containers:
  - name: oadp-mustgather-container
    image: registry.redhat.io/oadp/oadp-mustgather-rhel9:v1.3
    command: ["sleep"]
    args: ["infinity"]
```
The Kopia client is available in the `oadp-mustgather` image.

1. Create the pod by running the following command:
```bash
$ oc apply -f <pod_config_file_name>
```
Replace `<pod_config_file_name>` with the name of the YAML file for the pod configuration.

1. Verify that the Security Context Constraints (SCC) on the pod is `anyuid`, so that Kopia can connect to the repository.
```bash
$ oc describe pod/oadp-mustgather-pod | grep scc
```
.Example output

```bash
openshift.io/scc: anyuid
```

1. Connect to the pod via SSH by running the following command:
```bash
$ oc -n openshift-adp rsh pod/oadp-mustgather-pod
```

1. Connect to the Kopia repository by running the following command:
```bash
sh-5.1# kopia repository connect s3 \
  --bucket=<bucket_name> \
  --prefix=velero/kopia/<application_namespace> \
  --password=static-passw0rd \
  --access-key="<access_key>" \
  --secret-access-key="<secret_access_key>" \
  --endpoint=<bucket_endpoint>
```
where:
`<bucket_name>`:: Specifies the object storage provider bucket name.
`<application_namespace>`:: Specifies the namespace for the application.
`static-passw0rd`:: This is the Kopia password to connect to the repository.
`<access_key>`:: Specifies the object storage provider access key.
`<secret_access_key>`:: Specifies the object storage provider secret access key.
`<bucket_endpoint>`:: Specifies the bucket endpoint. You do not need to specify the bucket endpoint, if you are using AWS S3 as the storage provider.

This is an example command. The command can vary based on the object storage provider.

1. To benchmark the hashing algorithm, run the following command:
```bash
sh-5.1# kopia benchmark hashing
```
.Example output
```bash
Benchmarking hash 'BLAKE2B-256' (100 x 1048576 bytes, parallelism 1)
Benchmarking hash 'BLAKE2B-256-128' (100 x 1048576 bytes, parallelism 1)

Fastest option for this machine is: --block-hash=BLAKE3-256
```

1. To benchmark the encryption algorithm, run the following command:
```bash
sh-5.1# kopia benchmark encryption
```
.Example output
```bash
Benchmarking encryption 'AES256-GCM-HMAC-SHA256'
Benchmarking encryption 'CHACHA20-POLY1305-HMAC-SHA256'

Fastest option for this machine is: --encryption=AES256-GCM-HMAC-SHA256
```

1. To benchmark the splitter algorithm, run the following command:
```bash
sh-5.1# kopia benchmark splitter
```
.Example output
```bash
splitting 16 blocks of 32MiB each, parallelism 1
DYNAMIC                     747.6 MB/s count:107 min:9467 10th:2277562 25th:2971794 50th:4747177 75th:7603998 90th:8388608 max:8388608
DYNAMIC-128K-BUZHASH        718.5 MB/s count:3183 min:3076 10th:80896 25th:104312 50th:157621 75th:249115 90th:262144 max:262144
DYNAMIC-128K-RABINKARP      164.4 MB/s count:3160 min:9667 10th:80098 25th:106626 50th:162269 75th:250655 90th:262144 max:262144

```
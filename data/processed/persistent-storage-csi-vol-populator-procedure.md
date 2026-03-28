# Creating prepopulated volumes using volume populators

The following procedure explains how to create a prepopulated persistent volume claim (PVC)  using the example `hellos.hello.example.com` Custom Resource Definition (CRD) created previously. 

In this example, rather than using an actual data source, you are creating a file called "example.txt" that contains the string "Hello, world!" in the root directory of the volume. For a real-world implementation, you need to create your own volume populator.

.Prerequisites

- You are logged in to a running OpenShift Container Platform cluster.

- There is an existing custom resource definition (CRD) for volume populators.

- OpenShift Container Platform does not ship with any volume populators. You *must* create your own volume populator.

.Procedure

1. Create a Custom Resource (CR) instance of the `Hello` CRD with the text "Hello, World!" passed in as `fileContents` parameter by running the following command:
```bash
$ oc apply -f  - <<EOF
apiVersion: hello.example.com/v1alpha1
kind: Hello
metadata:
  name: example-hello
spec:
  fileName: example.txt
  fileContents: Hello, world!
EOF
```

1. Create a PVC that references the Hello CR similar to the following example file:
.Example PVC YAML file
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: example-pvc
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 10Mi
  dataSourceRef: <1>
    apiGroup: hello.example.com
    kind: Hello
    name: example-hello <2>
  volumeMode: Filesystem
```
<1> The `dataSourceRef` field specifies the data source for the PVC.
<2> The name of the CR that you are using as the data source. In this example, 'example-hello'.

.Verification

1. After a few minutes, ensure that the PVC is created and in the `Bound` status by running the following command:
```bash
$ oc get pvc example-pvc -n hello <1>
```
<1> In this example, the name of the PVC is `example-pvc`.
.Example output
```bash
NAME          STATUS    VOLUME        CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
example-pvc   Bound     my-pv         10Mi       ReadWriteOnce  gp3-csi        <unset>                 14s
```

1. Create a job that reads from the PVC to verify that the data source information was applied using the following example file:
.Example job YAML file
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: example-job
spec:
  template:
    spec:
      containers:
        - name: example-container
          image: busybox:latest
          command:
            - cat
            - /mnt/example.txt <1>
          volumeMounts:
            - name: vol
              mountPath: /mnt
      restartPolicy: Never
      volumes:
        - name: vol
          persistentVolumeClaim:
            claimName: example-pvc <2>
```
<1> The location and name of the file with the "Hello, world!" text.
<2> The name of the PVC you created in Step 2. In this example, `example-pvc`.

1. Start the job by running the following command:
```bash
$ oc run example-job --image=busybox --command -- sleep 30 --restart=OnFailure
```
.Example output
```bash
pod/example-job created
```

1. Wait for the job, and all of its dependencies, to finish by running the following command:
```bash
$ oc wait --for=condition=Complete pod/example-job
```

1. Verify the contents collected by the job by running the following command:
```bash
$ oc logs job/example-job
```
.Expected output
```bash
Hello, world!
```
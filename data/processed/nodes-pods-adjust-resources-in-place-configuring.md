# Configuring in-place pod resizing

In-place pod resizing requires that you add a resize policy to a pod specification. 

You cannot add or modify a resize policy in an existing pod, but you can add or edit the policy in the pod's owner object, such as a deployment, if the pod has an owner object. 

.Procedure

1. Create a pod spec with a resize policy or add a resize policy to the owner object of an existing pod:

.. Create a YAML file similar to the following example:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: resize-pod
spec:
# ...
  containers:
  - name: pause
    resizePolicy: <1>
    - resourceName: cpu
      restartPolicy: NotRequired
    - resourceName: memory
      restartPolicy: RestartContainer
# ...
```
<1> Specifies a resize policy. For CPU and/or memory resources specify one of the following values:
- `NotRequired`: Apply any resource changes without restarting the pod. This is the default when using a resize policy.
- `RestartContainer`: Apply any resource changes and restart the pod.

.. Create the object by running a command similar to the following:
```bash
$ oc create -f <file_name>.yaml
```

.Verification

- Check that the resize policy is applied by modifying the CPU or memory requests or limits by running a command similar to the following. You must include the `--subresource resize` flag. If the pod has a owner object, such as a deployment, you must edit the owner object. 
```bash
$ oc edit pod <pod_name>  --subresource resize
```
If the policy is applied, the pod responds as expected.
```bash
$ oc get pods
```
If the resize policy is `NotRequired`, the pod is not restarted.
.Example output
```bash
NAME                          READY   STATUS    RESTARTS     AGE
resize-pod                    1/1     Running   0            5s
```
If the resize policy is `RestartContainer`, the pod is restarted.
.Example output
```bash
NAME                         READY   STATUS    RESTARTS    AGE
resize-pod                   1/1     Running   1 (5s ago)  5s
```
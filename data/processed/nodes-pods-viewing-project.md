# Viewing pods in a project

You can display pod usage statistics, such as CPU, memory, and storage consumption, to monitor container runtime environments and ensure efficient resource use.

.Procedure

1. Change to the project by entering the following command:
```bash
$ oc project <project_name>
```

1. Obtain a list of pods by entering the following command:
```bash
$ oc get pods
```
.Example output
```bash
NAME                       READY   STATUS    RESTARTS   AGE
console-698d866b78-bnshf   1/1     Running   2          165m
console-698d866b78-m87pm   1/1     Running   2          165m
```

1. Optional: Add the `-o wide` flags to view the pod IP address and the node where the pod is located. For example:
```bash
$ oc get pods -o wide
```
.Example output
```bash
NAME                       READY   STATUS    RESTARTS   AGE    IP            NODE                           NOMINATED NODE
console-698d866b78-bnshf   1/1     Running   2          166m   10.128.0.24   ip-10-0-152-71.ec2.internal    <none>
console-698d866b78-m87pm   1/1     Running   2          166m   10.129.0.23   ip-10-0-173-237.ec2.internal   <none>
```
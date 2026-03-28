# Listing pods on a node in your cluster

You can list all of the pods on a node by using the `oc get pods` command along with specific flags. This command shows the number of pods on that node, the state of the pods, number of pod restarts, and the age of the pods.

.Procedure

- To list all or selected pods on selected nodes:
```bash
$ oc get pod --selector=<nodeSelector>
```
```bash
$ oc get pod --selector=kubernetes.io/os
```
Or:
```bash
$ oc get pod -l=<nodeSelector>
```
```bash
$ oc get pod -l kubernetes.io/os=linux
```

- To list all pods on a specific node, including terminated pods:
```bash
$ oc get pod --all-namespaces --field-selector=spec.nodeName=<nodename>
```
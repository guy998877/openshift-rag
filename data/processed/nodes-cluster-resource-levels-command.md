# Running the OpenShift Cluster Capacity Tool on the command line

You can run the OpenShift Cluster Capacity Tool from the command line to estimate the number of pods that can be scheduled onto your cluster.

You create a sample pod spec file, which the tool uses for estimating resource usage. The pod spec specifies its resource requirements as `limits` or `requests`. The cluster capacity tool takes the pod's resource requirements into account for its estimation analysis.

.Prerequisites

1. Run the OpenShift Cluster Capacity Tool, which is available as a container image from the Red Hat Ecosystem Catalog. See the link in the "Additional resources" section.

1. Create a sample pod spec file:

.. Create a YAML file similar to the following:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: small-pod
  labels:
    app: guestbook
    tier: frontend
spec:
  securityContext:
    runAsNonRoot: true
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: php-redis
    image: gcr.io/google-samples/gb-frontend:v4
    imagePullPolicy: Always
    resources:
      limits:
        cpu: 150m
        memory: 100Mi
      requests:
        cpu: 150m
        memory: 100Mi
    securityContext:
      allowPrivilegeEscalation: false
      capabilities:
        drop: [ALL]
```

.. Create the cluster role:
```bash
$ oc create -f <file_name>.yaml
```
For example:
```bash
$ oc create -f pod-spec.yaml
```

.Procedure

1. From the terminal, log in to the Red Hat Registry:
```bash
$ podman login registry.redhat.io
```

1. Pull the cluster capacity tool image:
```bash
$ podman pull registry.redhat.io/openshift4/ose-cluster-capacity
```

1. Run the cluster capacity tool:
```bash
$ podman run -v $HOME/.kube:/kube:Z -v $(pwd):/cc:Z  ose-cluster-capacity \
/bin/cluster-capacity --kubeconfig /kube/config --<pod_spec>.yaml /cc/<pod_spec>.yaml \
--verbose
```
--
where:

<pod_spec>.yaml:: Specifies the pod spec to use.

verbose:: Outputs a detailed description of how many pods can be scheduled on each node in the cluster.
--
.Example output
```bash
small-pod pod requirements:
	- CPU: 150m
	- Memory: 100Mi

The cluster can schedule 88 instance(s) of the pod small-pod.

Termination reason: Unschedulable: 0/5 nodes are available: 2 Insufficient cpu,
3 node(s) had taint {node-role.kubernetes.io/master: }, that the pod didn't
tolerate.

Pod distribution among nodes:
small-pod
	- 192.168.124.214: 45 instance(s)
	- 192.168.124.120: 43 instance(s)
```
In the above example, the number of estimated pods that can be scheduled onto
the cluster is 88.
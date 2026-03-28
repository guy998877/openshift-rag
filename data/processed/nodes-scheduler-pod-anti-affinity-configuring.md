# Configuring a pod anti-affinity rule

The following steps demonstrate a simple two-pod configuration that creates pod with a label and a pod that uses an anti-affinity preferred rule to attempt to prevent scheduling with that pod.

> **NOTE:** You cannot add an affinity directly to a scheduled pod.

.Procedure

1. Create a pod with a specific label in the pod spec:
.. Create a YAML file with the following content:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: security-s1
  labels:
    security: S1
spec:
  securityContext:
    runAsNonRoot: true
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: security-s1
    image: docker.io/ocpqe/hello-pod
    securityContext:
      allowPrivilegeEscalation: false
      capabilities:
        drop: [ALL]
```
.. Create the pod.
```bash
$ oc create -f <pod-spec>.yaml
```

1. When creating other pods, configure the following parameters:
.. Create a YAML file with the following content:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: security-s2-east
# ...
spec:
# ...
  affinity: <1>
    podAntiAffinity:
      preferredDuringSchedulingIgnoredDuringExecution: <2>
      - weight: 100 <3>
        podAffinityTerm:
          labelSelector:
            matchExpressions:
            - key: security <4>
              values:
              - S1
              operator: In <5>
          topologyKey: kubernetes.io/hostname <6>
# ...
```
<1> Adds a pod anti-affinity.
<2> Configures the `requiredDuringSchedulingIgnoredDuringExecution` parameter or the `preferredDuringSchedulingIgnoredDuringExecution` parameter.
<3> For a preferred rule, specifies a weight for the node, 1-100. The node that with highest weight is preferred.
<4> Specifies the `key` and `values` that must be met. If you want the new pod to not be scheduled with the other pod, use the same `key` and `values` parameters as the label on the first pod.
<5> Specifies an `operator`. The operator can be `In`, `NotIn`, `Exists`, or `DoesNotExist`. For example, use the operator `In` to require the label to be in the node.
<6> Specifies a `topologyKey`, which is a prepopulated [Kubernetes label](https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#interlude-built-in-node-labels) that the system uses to denote such a topology domain.

.. Create the pod.
```bash
$ oc create -f <pod-spec>.yaml
```
# Creating the ClusterPodPlacementConfig object by using the CLI

To deploy the pod placement operand that enables architecture-aware workload scheduling, you can create the `ClusterPodPlacementConfig` object by using the OpenShift CLI (`oc`).

.Prerequisites

- You have installed `oc`.
- You have logged in to `oc` as a user with `cluster-admin` privileges.
- You have installed the Multiarch Tuning Operator.

.Procedure

1. Create a `ClusterPodPlacementConfig` object YAML file:
.Example `ClusterPodPlacementConfig` object configuration
```yaml
apiVersion: multiarch.openshift.io/v1beta1
kind: ClusterPodPlacementConfig
metadata:
  name: cluster
spec:
  logVerbosityLevel: Normal
  namespaceSelector:
    matchExpressions:
      - key: multiarch.openshift.io/exclude-pod-placement 
        operator: DoesNotExist
  plugins:
    nodeAffinityScoring:
      enabled: true
      platforms:
        - architecture: amd64
          weight: 100
        - architecture: arm64
          weight: 50
```

1. Create the `ClusterPodPlacementConfig` object by running the following command:
```bash
$ oc create -f <file_name> <1>
```
<1> Replace `<file_name>` with the name of the `ClusterPodPlacementConfig` object YAML file.

.Verification

- To check that the `ClusterPodPlacementConfig` object is created, run the following command:
```bash
$ oc get clusterpodplacementconfig
```
.Example output
```bash
NAME      AGE
cluster   29s
```
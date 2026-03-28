By default, when you install an Operator, OpenShift Container Platform installs the Operator pod to one of your worker nodes randomly. However, there might be situations where you want that pod scheduled on a specific node or set of nodes.

The following examples describe situations where you might want to schedule an Operator pod to a specific node or set of nodes:

- If an Operator requires a particular platform, such as `amd64` or `arm64`
- If an Operator requires a particular operating system, such as Linux or Windows
- If you want Operators that work together scheduled on the same host or on hosts located on the same rack
- If you want Operators dispersed throughout the infrastructure to avoid downtime due to network or hardware issues

.Procedure

To control the placement of an Operator pod, complete the following steps:

1. Install the Operator as usual.

1. If needed, ensure that your nodes are labeled to properly respond to the affinity.

1. Edit the Operator `Subscription` object to add an affinity:

.Verification

- To ensure that the pod is deployed on the specific node, run the following command:
```yaml
$ oc get pods -o wide
```
.Example output
```bash
NAME                                                  READY   STATUS    RESTARTS   AGE   IP            NODE                           NOMINATED NODE   READINESS GATES
custom-metrics-autoscaler-operator-5dcc45d656-bhshg   1/1     Running   0          50s   10.131.0.20   ip-10-0-185-229.ec2.internal   <none>           <none>
```
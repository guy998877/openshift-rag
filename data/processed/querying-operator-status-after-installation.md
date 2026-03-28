# Querying Operator status after installation

You can check Operator status at the end of an installation. Retrieve diagnostic data for Operators that do not become available. Review logs for any Operator pods that are listed as `Pending` or have an error status. Validate base images used by problematic pods.

.Prerequisites

- You have access to the cluster as a user with the `cluster-admin` role.
- You have installed the OpenShift CLI (`oc`).

.Procedure

1. Check that cluster Operators are all available at the end of an installation.
```bash
$ oc get clusteroperators
```

1. Verify that all of the required certificate signing requests (CSRs) are approved. Some nodes might not move to a `Ready` status and some cluster Operators might not become available if there are pending CSRs.
.. Check the status of the CSRs and ensure that you see a client and server request with the `Pending` or `Approved` status for each machine that you added to the cluster:
```bash
$ oc get csr
```
.Example output
```bash
NAME        AGE     REQUESTOR                                                                   CONDITION
csr-8b2br   15m     system:serviceaccount:openshift-machine-config-operator:node-bootstrapper   Pending
csr-8vnps   15m     system:serviceaccount:openshift-machine-config-operator:node-bootstrapper   Pending
csr-bfd72   5m26s   system:node:ip-10-0-50-126.us-east-2.compute.internal                       Pending
csr-c57lv   5m26s   system:node:ip-10-0-95-157.us-east-2.compute.internal                       Pending
...
```
- In this example, `csr-8b2br` represents a client request CSR.
- The `csr-bfd72` represents a server request CSR.
In this example, two machines are joining the cluster. You might see more approved CSRs in the list.
.. If the CSRs were not approved, after all of the pending CSRs for the machines you added are in `Pending` status, approve the CSRs for your cluster machines:
> **NOTE:** Because the CSRs rotate automatically, approve your CSRs within an hour of adding the machines to the cluster. If you do not approve them within an hour, the certificates will rotate, and more than two certificates will be present for each node. You must approve all of these certificates. After you approve the initial CSRs, the subsequent node client CSRs are automatically approved by the cluster `kube-controller-manager`.
> **NOTE:** For clusters running on platforms that are not machine API enabled, such as bare metal and other user-provisioned infrastructure, you must implement a method of automatically approving the kubelet serving certificate requests (CSRs). If a request is not approved, then the `oc exec`, `oc rsh`, and `oc logs` commands cannot succeed, because a serving certificate is required when the API server connects to the kubelet. Any operation that contacts the Kubelet endpoint requires this certificate approval to be in place. The method must watch for new CSRs, confirm that the CSR was submitted by the `node-bootstrapper` service account in the `system:node` or `system:admin` groups, and confirm the identity of the node.

- To approve them individually, run the following command for each valid CSR:
```bash
$ oc adm certificate approve <csr_name>
```

- To approve all pending CSRs, run the following command:
```bash
$ oc get csr -o go-template='{{range .items}}{{if not .status}}{{.metadata.name}}{{"\n"}}{{end}}{{end}}' | xargs oc adm certificate approve
```

1. View Operator events:
```bash
$ oc describe clusteroperator <operator_name>
```

1. Review Operator pod status within the Operator's namespace:
```bash
$ oc get pods -n <operator_namespace>
```

1. Obtain a detailed description for pods that do not have `Running` status:
```bash
$ oc describe pod/<operator_pod_name> -n <operator_namespace>
```

1. Inspect pod logs:
```bash
$ oc logs pod/<operator_pod_name> -n <operator_namespace>
```

1. When experiencing pod base image related issues, review base image status.
.. Obtain details of the base image used by a problematic pod:
```bash
$ oc get pod -o "jsonpath={range .status.containerStatuses[*]}{.name}{'\t'}{.state}{'\t'}{.image}{'\n'}{end}" <operator_pod_name> -n <operator_namespace>
```
.. List base image release information:
```bash
$ oc adm release info <image_path>:<tag> --commits
```
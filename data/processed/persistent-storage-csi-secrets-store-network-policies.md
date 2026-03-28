# Support for network policies

The Secrets Store CSI Driver Operator includes pre-defined `NetworkPolicies` resources for enhanced security. These policies govern the ingress and egress traffic for both the SS-CSI Operator and its associated driver.

The following table summarizes the default ingress and egress rules:

[cols="1,1,1,1", options="header"]
|===
| Component | Ingress ports | Egress ports | Description

| Secrets Store CSI Driver Operator
| `8443`
| `6443`
| Accesses metrics and communicates with the API server

| Secrets Store CSI driver
| `8095`
| `6443`
| Accesses metrics and communicates with the API server
|===
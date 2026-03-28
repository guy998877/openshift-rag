# Verifying access to Red Hat Hybrid Cloud Console for private OpenShift Container Platform clusters

The console of the private cluster is private by default. During cluster installation, the default Ingress Controller managed by OpenShift's Ingress Operator is configured with an internal AWS Network Load Balancer (NLB).

.Procedure

- If your private OpenShift Container Platform cluster shows a `ready` status but you cannot access the OpenShift Container Platform web console for the cluster, try accessing the cluster console from either within the cluster VPC or from a network that is connected to the VPC.
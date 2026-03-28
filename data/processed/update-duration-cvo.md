# Cluster Version Operator target update payload deployment

In the first phase of the update, the Cluster Version Operator (CVO) retrieves the target update release image and applies to the cluster.

All components which run as pods are updated during this phase, whereas the host components are updated by the Machine Config Operator (MCO). This process might take 60 to 120 minutes.

> **NOTE:** The CVO phase of the update does not restart the nodes.
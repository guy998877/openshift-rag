# Adding bare-metal nodes

Adding bare-metal nodes to an OpenShift Container Platform cluster on vSphere is supported as a Technology Preview feature. 

However, if you add bare-metal nodes, you must remove the vSphere CSI Driver, otherwise the cluster is marked as degraded. For information about how to remove the driver and the consequences of doing this, see Section _Disabling and enabling storage on vSphere_. 

For information about how to add bare-metal nodes, under _Additional resources_, see Section _Adding bare-metal compute machines to a vSphere cluster_.
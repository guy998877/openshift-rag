# Machine API overview

The Machine API is a combination of primary resources that are based on the upstream Cluster API project and custom OpenShift Container Platform resources.

For OpenShift Container Platform 4.21 clusters, the Machine API performs all node host provisioning management actions after the cluster installation finishes. Because of this system, OpenShift Container Platform 4.21 offers an elastic, dynamic provisioning method on top of public or private cloud infrastructure.

The two primary resources are:

Machines:: A fundamental unit that describes the host for a node. A machine has a `providerSpec` specification, which describes the types of compute nodes that are offered for different cloud platforms. For example, a machine type for a compute node might define a specific machine type and required metadata.

Machine sets:: `MachineSet` resources are groups of compute machines. Compute machine sets are to compute machines as replica sets are to pods. If you need more compute machines or must scale them down, you change the `replicas` field on the `MachineSet` resource to meet your compute need.
> **WARNING:** Control plane machines cannot be managed by compute machine sets. Control plane machine sets provide management capabilities for supported control plane machines that are similar to what compute machine sets provide for compute machines. For more information, see “Managing control plane machines".

The following custom resources add more capabilities to your cluster:

Machine autoscaler:: The `MachineAutoscaler` resource automatically scales compute machines in a cloud. You can set the minimum and maximum scaling boundaries for nodes in a specified compute machine set, and the machine autoscaler maintains that range of nodes.
The `MachineAutoscaler` object takes effect after a `ClusterAutoscaler` object exists. Both `ClusterAutoscaler` and `MachineAutoscaler` resources are made available by the `ClusterAutoscalerOperator` object.

Cluster autoscaler:: This resource is based on the upstream cluster autoscaler project. In the OpenShift Container Platform implementation, it is integrated with the Machine API by extending the compute machine set API. You can use the cluster autoscaler to manage your cluster in the following ways:
- Set cluster-wide scaling limits for resources such as cores, nodes, memory, and GPU
- Set the priority so that the cluster prioritizes pods and new nodes are not brought online for less important pods
- Set the scaling policy so that you can scale up nodes but not scale them down

Machine health check:: The `MachineHealthCheck` resource detects when a machine is unhealthy, deletes it, and, on supported platforms, makes a new machine.

// Should this paragraph still be in here in 2022? Or at least should it be rephrased to avoid comparing to 3.11?
In OpenShift Container Platform version 3.11, you could not roll out a multi-zone architecture easily because the cluster did not manage machine provisioning. Beginning with OpenShift Container Platform version 4.1, this process is easier. Each compute machine set is scoped to a single zone, so the installation program sends out compute machine sets across availability zones on your behalf. And then because your compute is dynamic, and in the face of a zone failure, you always have a zone for when you must rebalance your machines. In global Azure regions that do not have multiple availability zones, you can use availability sets to ensure high availability. The autoscaler provides best-effort balancing over the life of a cluster.
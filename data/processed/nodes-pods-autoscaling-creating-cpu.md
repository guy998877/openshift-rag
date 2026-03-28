# Creating a horizontal pod autoscaler by using the CLI

Using the OpenShift Container Platform CLI, you can create a horizontal pod autoscaler (HPA) to automatically scale an existing `Deployment`, `DeploymentConfig`, `ReplicaSet`, `ReplicationController`, or `StatefulSet` object. The HPA scales the pods associated with that object to maintain the CPU or memory resources that you specify.

You can autoscale based on CPU or memory use by specifying a percentage of resource usage or a specific value, as described in the following sections.

The HPA increases and decreases the number of replicas between the minimum and maximum numbers to maintain the specified resource use across all pods.
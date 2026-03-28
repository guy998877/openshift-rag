# Cluster Operators

In OpenShift Container Platform, all cluster functions are divided into a series of default _cluster Operators_. Cluster Operators manage a particular area of cluster functionality, such as cluster-wide application logging, management of the Kubernetes control plane, or the machine provisioning system.

Cluster Operators are represented by a `ClusterOperator` object, which
cluster administrators
can view in the OpenShift Container Platform web console from the *Administration* -> *Cluster Settings* page. Each cluster Operator provides a simple API for determining cluster functionality. The Operator hides the details of managing the lifecycle of that component. Operators can manage a single component or tens of components, but the end goal is always to reduce operational burden by automating common actions.
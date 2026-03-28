# Add-on Operators

Operator Lifecycle Manager (OLM) and the software catalog are default components in OpenShift Container Platform that help manage Kubernetes-native applications as Operators. Together they provide the system for discovering, installing, and managing the optional add-on Operators available on the cluster.

Using the software catalog in the OpenShift Container Platform web console,
cluster administrators
and authorized users can select Operators to install from catalogs of Operators. After installing an Operator from the software catalog, it can be made available globally or in specific namespaces to run in user applications.

Default catalog sources are available that include Red Hat Operators, certified Operators, and community Operators.
Cluster administrators
can also add their own custom catalog sources, which can contain a custom set of Operators.

> **NOTE:** OLM does not manage the cluster Operators that comprise the OpenShift Container Platform architecture.
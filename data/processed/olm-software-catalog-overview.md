# About the software catalog

The _software catalog_ is the web console interface in OpenShift Container Platform that cluster administrators use to discover and install Operators. With one click, an Operator can be pulled from its off-cluster source, installed and subscribed on the cluster, and made ready for engineering teams to self-service manage the product across deployment environments using Operator Lifecycle Manager (OLM).

Cluster administrators can choose from catalogs grouped into the following categories:

[cols="2a,8a",options="header"]
|===
|Category |Description

|Red Hat Operators
|Red Hat products packaged and shipped by Red Hat. Supported by Red Hat.

|Certified Operators
|Products from leading independent software vendors (ISVs). Red Hat partners with ISVs to package and ship. Supported by the ISV.

// |Red Hat Marketplace
// |Certified software that can be purchased from [Red Hat Marketplace](https://marketplace.redhat.com/).

|Community Operators
|Optionally-visible software maintained by relevant representatives in the [redhat-openshift-ecosystem/community-operators-prod/operators](https://github.com/redhat-openshift-ecosystem/community-operators-prod/tree/main/operators) GitHub repository. No official support.

|Custom Operators
|Operators you add to the cluster yourself. If you have not added any custom Operators, the *Custom* category does not appear in the web console software catalog.
|===

Operators in the software catalog are packaged to run on OLM. This includes a YAML file called a cluster service version (CSV) containing all of the CRDs, RBAC rules, deployments, and container images required to install and securely run the Operator. It also contains user-visible information like a description of its features and supported Kubernetes versions.
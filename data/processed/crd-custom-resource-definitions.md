# Custom resource definitions

In the Kubernetes API, a _resource_ is an endpoint that stores a collection of API objects of a certain kind. For example, the built-in `Pods` resource contains a collection of `Pod` objects.

A _custom resource definition_ (CRD) object defines a new, unique object type, called a _kind_, in the cluster and lets the Kubernetes API server handle its entire lifecycle.

_Custom resource_ (CR) objects are created from CRDs that have been added to the cluster by a cluster administrator, allowing all cluster users to add the new resource type into projects.

Operators in particular make use of CRDs by packaging them with any required RBAC policy and other software-specific logic.
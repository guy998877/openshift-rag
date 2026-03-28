# About identity providers in OpenShift Container Platform

By default, only a `kubeadmin` user exists on your cluster. To specify an
identity provider, you must create a custom resource (CR) that describes
that identity provider and add it to the cluster.

> **NOTE:** OpenShift Container Platform user names containing `/`, `:`, and `%` are not supported.
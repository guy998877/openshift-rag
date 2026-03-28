# Introduction to OpenShift Container Platform

OpenShift Container Platform is a platform for developing and running containerized applications. It is designed to allow applications and the data centers that support them to expand from just a few machines and applications to thousands of machines that serve millions of clients.

With its foundation in Kubernetes, OpenShift Container Platform incorporates the same technology that serves as the engine for massive telecommunications, streaming video, gaming, banking, and other applications. Its implementation in open
Red Hat technologies lets you extend your containerized applications beyond a single cloud to on-premise and multi-cloud environments.

image::525-OpenShift-arch-012025.png[Red Hat OpenShift Kubernetes Engine]

// The architecture presented here is meant to give you insights into how OpenShift Container Platform works. It does this by stepping you through the process of installing an OpenShift Container Platform cluster, managing the cluster, and developing and deploying applications on it. Along the way, this architecture describes:

// * Major components of  OpenShift Container Platform
// * Ways of exploring different aspects of OpenShift Container Platform yourself
// * Available frontdoors (and backdoors) to modify the installation and management of your OpenShift Container Platform cluster
// * Different types of container application types
# OpenShift Container Platform overview

////
Red Hat was one of the early contributors of Kubernetes and quickly integrated
it as the centerpiece of its OpenShift Container Platform product line. Today, Red Hat
continues as one of the largest contributors to Kubernetes across a wide range
of technology areas.
////

OpenShift Container Platform provides enterprise-ready enhancements to Kubernetes, including the following enhancements:

- Integrated Red Hat technology. Major components in OpenShift Container Platform come from Red Hat Enterprise Linux (RHEL) and related Red Hat technologies. OpenShift Container Platform benefits from the intense testing and certification initiatives for Red Hat's enterprise quality software.
- Open source development model. Development is completed in the open, and the source code is available from public software repositories. This open collaboration fosters rapid innovation and development.

Although Kubernetes excels at managing your applications, it does not specify
or manage platform-level requirements or deployment processes. Powerful and
flexible platform management tools and processes are important benefits that
OpenShift Container Platform 4.21 offers. The following sections describe some
unique features and benefits of OpenShift Container Platform.

## Custom operating system

OpenShift Container Platform uses Red Hat Enterprise Linux CoreOS (RHCOS), a container-oriented operating system that is specifically designed for running containerized applications from OpenShift Container Platform and works with new tools to provide fast installation, Operator-based management, and simplified upgrades.

RHCOS includes:

- Ignition, which OpenShift Container Platform uses as a firstboot system configuration for initially bringing up and configuring machines.
- CRI-O, a Kubernetes native container runtime implementation that integrates closely with the operating system to deliver an efficient and optimized Kubernetes experience. CRI-O provides facilities for running, stopping, and restarting containers. It fully replaces the Docker Container Engine, which was used in OpenShift Container Platform 3.
- Kubelet, the primary node agent for Kubernetes that is responsible for
launching and monitoring containers.

In OpenShift Container Platform 4.21, you must use RHCOS for all control
plane machines, but you can use Red Hat Enterprise Linux (RHEL) as the operating
system for compute machines, which are also known as worker machines. If you choose to use RHEL workers, you
must perform more system maintenance than if you use RHCOS for all of the
cluster machines.

## Simplified installation and update process

With OpenShift Container Platform 4.21, if you have an account with the right
permissions, you can deploy a production cluster in supported clouds by running
a single command and providing a few values. You can also customize your cloud
installation or install your cluster in your data center if you use a supported
platform.

For clusters that use RHCOS for all machines, updating, or
upgrading, OpenShift Container Platform is a simple, highly-automated process. Because
OpenShift Container Platform completely controls the systems and services that run on each
machine, including the operating system itself, from a central control plane,
upgrades are designed to become automatic events. If your cluster contains
RHEL worker machines, the control plane benefits from the streamlined update
process, but you must perform more tasks to upgrade the RHEL machines.

## Other key features

Operators are both the fundamental unit of the OpenShift Container Platform 4.21
code base and a convenient way to deploy applications and software components
for your applications to use. In OpenShift Container Platform, Operators serve as the platform foundation and remove the need for manual upgrades of operating systems and control plane applications. OpenShift Container Platform Operators such as the
Cluster Version Operator and Machine Config Operator allow simplified,
cluster-wide management of those critical components.

Operator Lifecycle Manager (OLM) and the software catalog provide facilities for
storing and distributing Operators to people developing and deploying applications.

The Red Hat Quay Container Registry is a Quay.io container registry that serves
most of the container images and Operators to OpenShift Container Platform clusters.
Quay.io is a public registry version of Red Hat Quay that stores millions of images
and tags.

Other enhancements to Kubernetes in OpenShift Container Platform include improvements in
software defined networking (SDN), authentication, log aggregation, monitoring,
and routing. OpenShift Container Platform also offers a comprehensive web console and the
custom OpenShift CLI (`oc`) interface.

////
OpenShift Container Platform includes the following infrastructure components:

- OpenShift API server
- Kubernetes API server
- Kubernetes controller manager
- Kubernetes nodes/kubelet
- CRI-O
- RHCOS
- Infrastructure Operators
- Networking (SDN/Router/DNS)
- Storage
- Monitoring
- Telemetry
- Security
- Authorization/Authentication/Oauth
- Logging

It also offers the following user interfaces:
- Web Console
- OpenShift CLI (`oc`)
- Rest API
////

## OpenShift Container Platform lifecycle

The following figure illustrates the basic OpenShift Container Platform lifecycle:

- Creating an OpenShift Container Platform cluster
- Managing the cluster
- Developing and deploying applications
- Scaling up applications

.High level OpenShift Container Platform overview
image::ocp_arch_lifecycle.png[High-level OpenShift Container Platform flow]
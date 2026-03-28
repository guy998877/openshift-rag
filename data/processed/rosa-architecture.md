# OpenShift Container Platform

In OpenShift Container Platform, both the control plane and the worker nodes are deployed in your VPC subnets.

## OpenShift Container Platform on public and private networks

With OpenShift Container Platform, you can create clusters that are accessible over public or private networks.

You can customize access patterns for your API server endpoint and Red Hat SRE management in the following ways:

- Public - API server endpoint and application routes are internet-facing.

- Private - API server endpoint and application routes are private. Private OpenShift Container Platform clusters use some public subnets, but no control plane or worker nodes are deployed in public subnets.

- Private with AWS PrivateLink - API server endpoint and application routes are private. Public subnets or NAT gateways are not required in your VPC for egress. OpenShift Container Platform SRE management uses AWS PrivateLink.

The following image depicts the architecture of a OpenShift Container Platform cluster deployed on both public and private networks.

.OpenShift Container Platform deployed on public and private networks
image::156_OpenShift_ROSA_Arch_0621_private_public_classic.png[OpenShift Container Platform on public and private networks]

OpenShift Container Platform clusters include infrastructure nodes where OpenShift components such as the ingress controller, image registry, and monitoring are deployed. The infrastructure nodes and the OpenShift components deployed on them are managed by OpenShift Container Platform SREs.

The following types of clusters are available with OpenShift Container Platform:

- Single zone cluster - The control plane and worker nodes are hosted on a single availability zone.

- Multi-zone cluster - The control plane is hosted on three availability zones with an option to run worker nodes on one or three availability zones.
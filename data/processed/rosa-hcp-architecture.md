# OpenShift Container Platform architecture

OpenShift Container Platform hosts a highly-available, single-tenant OpenShift control plane. The hosted control plane is deployed across 3 availability zones with 2 API server instances and 3 etcd instances.

You can create a OpenShift Container Platform cluster with or without an internet-facing API server, with the latter considered a “private” cluster and the former considered a “public” cluster. Private API servers are only accessible from your VPC subnets. You access the hosted control plane through an AWS PrivateLink endpoint regardless of API privacy.

The worker nodes are deployed in your AWS account and run on your VPC private subnets. You can add additional private subnets from one or more availability zones to ensure high availability. Worker nodes are shared by OpenShift components and applications. OpenShift components such as the ingress controller, image registry, and monitoring are deployed on the worker nodes hosted on your VPC.

.OpenShift Container Platform architecture
image::544_OpenShift_ROSA-HCP_architecture-model.png[OpenShift Container Platform architecture]

## OpenShift Container Platform architecture on public and private networks
With OpenShift Container Platform, you can create your clusters on public or private networks. The following images depict the architecture of both public and private networks.

.OpenShift Container Platform deployed on a public network
image::544_OpenShift_ROSA-HCP-and-ROSA-Classic-public.png[OpenShift Container Platform deployed on a public network]

.OpenShift Container Platform deployed on a private network
image::544_OpenShift_ROSA-HCP-and-ROSA-Classic-private.png[OpenShift Container Platform deployed on a private network]
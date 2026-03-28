# Private OpenShift Container Platform on {GCP} without Private Service Connect (PSC) architecture model

With a private network configuration, your cluster API server endpoint and application routes are private. Private OpenShift Container Platform on Google Cloud clusters use some public subnets, but no control plane or worker nodes are deployed in public subnets.

> **IMPORTANT:** Red Hat recommends using Private Service Connect (PSC) when deploying a private OpenShift Container Platform cluster on {GCP}. PSC ensures there is a secured, private connectivity between Red Hat infrastructure, Site Reliability Engineering (SRE), and private OpenShift clusters.

Red Hat SRE management access the cluster through a public load balancer endpoint that are restricted to Red Hat IPs. The API server endpoint is private. A separate Red Hat API server endpoint is public (but restricted to Red Hat trusted IP addresses). The default ingress controller can be public or private. The following image shows network connectivity of a private cluster without Private Service Connect (PSC).

.OpenShift Container Platform on {GCP} deployed on a private network without PSC
image::484_b_Openshift_osd_gcp_private_no_psc_arch_0525.png[Private without PSC architecture model]
# Private OpenShift Container Platform on {GCP} architecture on public and private networks

You can customize the access patterns for your API server endpoint and Red Hat SRE management by choosing one of the following network configuration types:

- Private cluster with Private Service Connect (PSC).
- Private cluster without PSC
- Public cluster

> **IMPORTANT:** Red Hat recommends using PSC when deploying a private OpenShift Container Platform cluster on {GCP}. PSC ensures there is a secured, private connectivity between Red Hat infrastructure, Site Reliability Engineering (SRE), and private OpenShift clusters.
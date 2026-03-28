# OLM-managed Operator support for authentication with GCP Workload Identity

Certain Operators managed by the Operator Lifecycle Manager (OLM) on Google Cloud clusters can use manual mode with GCP Workload Identity. 
These Operators authenticate with limited-privilege, short-term credentials that are managed outside the cluster. 
To determine if an Operator supports authentication with GCP Workload Identity, see the Operator description in the software catalog.
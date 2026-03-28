# OLM-managed Operator support for authentication with AWS STS

Certain Operators managed by the Operator Lifecycle Manager (OLM) on AWS clusters can use manual mode with STS. 
These Operators authenticate with limited-privilege, short-term credentials that are managed outside the cluster. 
To determine if an Operator supports authentication with AWS STS, see the Operator description in the software catalog.
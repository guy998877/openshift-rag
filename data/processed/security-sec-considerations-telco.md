# Security considerations

Workloads might handle sensitive data and demand high reliability. A single security vulnerability might lead to broader, cluster-wide compromises. With numerous components running on an OpenShift Container Platform cluster, you must secure each component to prevent any breach from escalating. Ensuring security across the entire infrastructure, including all components, is essential to maintaining the integrity of the network and avoiding vulnerabilities.

The following key security features are essential for all industries that handle sensitive data:

- Security Context Constraints (SCCs): Provide granular control over pod security in the OpenShift Container Platform clusters.
- Pod Security Admission (PSA): Kubernetes-native pod security controls.
- Encryption: Ensures data confidentiality in high-throughput network environments.
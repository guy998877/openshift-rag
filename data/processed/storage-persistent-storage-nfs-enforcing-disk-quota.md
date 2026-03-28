# Enforce disk quotas

You can use disk partitions to enforce disk quotas and size constraints.
Each partition can be its own export. Each export is one PV.
OpenShift Container Platform enforces unique names for PVs, but the uniqueness of the
NFS volume's server and path is up to the administrator.

Enforcing quotas in this way allows the developer to request persistent
storage by a specific amount, such as 10Gi, and be matched with a
corresponding volume of equal or greater capacity.
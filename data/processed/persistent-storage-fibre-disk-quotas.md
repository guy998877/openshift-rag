# Enforcing disk quotas

Use LUN partitions to enforce disk quotas and size constraints.
Each LUN is mapped to a single persistent volume, and unique
names must be used for persistent volumes.

Enforcing quotas in this way allows the end user to request persistent storage
by a specific amount, such as 10Gi, and be matched with a corresponding volume
of equal or greater capacity.
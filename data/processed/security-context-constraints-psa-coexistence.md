# Pod security admission and security context constraints

Pod security admission standards and security context constraints are reconciled and enforced by two independent controllers. The two controllers work independently using the following processes to enforce security policies:

1. The security context constraint controller may mutate some security context fields per the pod's assigned SCC. For example, if the seccomp profile is empty or not set and if the pod's assigned SCC enforces `seccompProfiles` field to be `runtime/default`, the controller sets the default type to `RuntimeDefault`.

1. The security context constraint controller validates the pod's security context against the matching SCC.

1. The pod security admission controller validates the pod's security context against the pod security standard assigned to the namespace.
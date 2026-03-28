# Understanding pods

Pods are the rough equivalent of a machine instance (physical or virtual) to a Container. Each pod is allocated its own internal IP address, therefore owning its entire port space, and containers within pods can share their local storage and networking.

Pods have a lifecycle; they are defined, then they are assigned to run on
a node, then they run until their container(s) exit or they are removed
for some other reason. Pods, depending on policy and exit code, might be
removed after exiting, or can be retained to enable access to
the logs of their containers.

OpenShift Container Platform treats pods as largely immutable; changes cannot be made to
a pod definition while it is running. OpenShift Container Platform implements changes by
terminating an existing pod and recreating it with modified configuration,
base image(s), or both. Pods are also treated as expendable, and do not
maintain state when recreated. Therefore pods should usually be managed by
higher-level controllers, rather than directly by users.

> **NOTE:** For the maximum number of pods per OpenShift Container Platform node host, see the Cluster Limits.

> **WARNING:** Bare pods that are not managed by a replication controller will be not rescheduled upon node disruption.
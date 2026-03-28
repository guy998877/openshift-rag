# Persistent volume claim naming

To avoid resource conflicts, review the naming convention for automatically created persistent volume claims (PVCs). Because the system generates names by combining the pod name and volume name with a hyphen, you must ensure manually created resources do not inadvertently match this pattern.

For example, `pod-a` with volume `scratch` and `pod` with volume `a-scratch` both end up with the same PVC name, `pod-a-scratch`.

Such conflicts are detected, and a PVC is only used for an ephemeral volume if it was created for the pod. This check is based on the ownership relationship. An existing PVC is not overwritten or modified, but this does not resolve the conflict. Without the right PVC, a pod cannot start.

> **IMPORTANT:** Be careful when naming pods and volumes inside the same namespace so that naming conflicts do not occur.
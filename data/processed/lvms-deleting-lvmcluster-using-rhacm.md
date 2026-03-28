# Deleting an LVMCluster CR by using RHACM

If you have installed LVM Storage by using Red Hat Advanced Cluster Management (RHACM), you can delete an `LVMCluster` CR by using RHACM.

.Prerequisites

- You have access to the RHACM cluster as a user with `cluster-admin` permissions.
- You have deleted the persistent volume claims (PVCs), volume snapshots, and volume clones provisioned by LVM Storage. You have also deleted the applications that are using these resources.

.Procedure

1. Log in to the RHACM CLI using your OpenShift Container Platform credentials.
1. Delete the `ConfigurationPolicy` CR YAML file that was created for the `LVMCluster` CR:
```bash
$ oc delete -f <file_name> -n <cluster_namespace> <1>
```
<1> Namespace of the OpenShift Container Platform cluster on which LVM Storage is installed.

1. Create a `Policy` CR YAML file to delete the `LVMCluster` CR:
.Example `Policy` CR to delete the `LVMCluster` CR
```yaml
apiVersion: policy.open-cluster-management.io/v1
kind: Policy
metadata:
  name: policy-lvmcluster-delete
  annotations:
    policy.open-cluster-management.io/standards: NIST SP 800-53
    policy.open-cluster-management.io/categories: CM Configuration Management
    policy.open-cluster-management.io/controls: CM-2 Baseline Configuration
spec:
  remediationAction: enforce
  disabled: false
  policy-templates:
    - objectDefinition:
        apiVersion: policy.open-cluster-management.io/v1
        kind: ConfigurationPolicy
        metadata:
          name: policy-lvmcluster-removal
        spec:
          remediationAction: enforce <1>
          severity: low
          object-templates:
            - complianceType: mustnothave
              objectDefinition:
                kind: LVMCluster
                apiVersion: lvm.topolvm.io/v1alpha1
                metadata:
                  name: my-lvmcluster
                  namespace: openshift-lvm-storage <2>
---
apiVersion: policy.open-cluster-management.io/v1
kind: PlacementBinding
metadata:
  name: binding-policy-lvmcluster-delete
placementRef:
  apiGroup: apps.open-cluster-management.io
  kind: PlacementRule
  name: placement-policy-lvmcluster-delete
subjects:
  - apiGroup: policy.open-cluster-management.io
    kind: Policy
    name: policy-lvmcluster-delete
---
apiVersion: apps.open-cluster-management.io/v1
kind: PlacementRule
metadata:
  name: placement-policy-lvmcluster-delete
spec:
  clusterConditions:
    - status: "True"
      type: ManagedClusterConditionAvailable
  clusterSelector: <3>
    matchExpressions:
      - key: mykey
        operator: In
        values:
          - myvalue
```
<1> The `spec.remediationAction` in `policy-template` is overridden by the preceding parameter value for `spec.remediationAction`.
<2> This `namespace` field must have the `openshift-lvm-storage` value.
<3> Configure the requirements to select the clusters. LVM Storage is uninstalled on the clusters that match the selection criteria. 

1. Create the `Policy` CR by running the following command:
```bash
$ oc create -f <file_name> -n <namespace>
```

1. Create a `Policy` CR YAML file to check if the `LVMCluster` CR has been deleted:
.Example `Policy` CR to check if the `LVMCluster` CR has been deleted
```yaml
apiVersion: policy.open-cluster-management.io/v1
kind: Policy
metadata:
  name: policy-lvmcluster-inform
  annotations:
    policy.open-cluster-management.io/standards: NIST SP 800-53
    policy.open-cluster-management.io/categories: CM Configuration Management
    policy.open-cluster-management.io/controls: CM-2 Baseline Configuration
spec:
  remediationAction: inform
  disabled: false
  policy-templates:
    - objectDefinition:
        apiVersion: policy.open-cluster-management.io/v1
        kind: ConfigurationPolicy
        metadata:
          name: policy-lvmcluster-removal-inform
        spec:
          remediationAction: inform <1>
          severity: low
          object-templates:
            - complianceType: mustnothave
              objectDefinition:
                kind: LVMCluster
                apiVersion: lvm.topolvm.io/v1alpha1
                metadata:
                  name: my-lvmcluster
                  namespace: openshift-lvm-storage <2>
---
apiVersion: policy.open-cluster-management.io/v1
kind: PlacementBinding
metadata:
  name: binding-policy-lvmcluster-check
placementRef:
  apiGroup: apps.open-cluster-management.io
  kind: PlacementRule
  name: placement-policy-lvmcluster-check
subjects:
  - apiGroup: policy.open-cluster-management.io
    kind: Policy
    name: policy-lvmcluster-inform
---
apiVersion: apps.open-cluster-management.io/v1
kind: PlacementRule
metadata:
  name: placement-policy-lvmcluster-check
spec:
  clusterConditions:
    - status: "True"
      type: ManagedClusterConditionAvailable
  clusterSelector:
    matchExpressions:
      - key: mykey
        operator: In
        values:
          - myvalue
```
<1> The `policy-template` `spec.remediationAction` is overridden by the preceding parameter value for `spec.remediationAction`.
<2> The `namespace` field must have the `openshift-lvm-storage` value.

1. Create the `Policy` CR by running the following command:
```bash
$ oc create -f <file_name> -n <namespace>
```

.Verification

- Check the status of the `Policy` CRs by running the following command:
```bash
$ oc get policy -n <namespace>
```
.Example output
```bash
NAME                       REMEDIATION ACTION   COMPLIANCE STATE   AGE
policy-lvmcluster-delete   enforce              Compliant          15m
policy-lvmcluster-inform   inform               Compliant          15m
```
> **IMPORTANT:** The `Policy` CRs must be in `Compliant` state.
# Installing LVM Storage by using RHACM

To install LVM Storage on the clusters by using Red Hat Advanced Cluster Management (RHACM), you must create a `Policy` custom resource (CR). You can also configure the criteria to select the clusters on which you want to install LVM Storage.

> **NOTE:** The `Policy` CR that is created to install LVM Storage is also applied to the clusters that are imported or created after creating the `Policy` CR.

.Prerequisites
- You have access to the RHACM cluster using an account with `cluster-admin` and Operator installation permissions.
- You have dedicated disks that LVM Storage can use on each cluster.
- The cluster must be managed by RHACM.

.Procedure

1. Log in to the RHACM CLI using your OpenShift Container Platform credentials.

1. Create a namespace.
```bash
$ oc create ns <namespace>
```

1. Create a `Policy` CR YAML file:
.Example `Policy` CR to install and configure LVM Storage
```yaml
apiVersion: apps.open-cluster-management.io/v1
kind: PlacementRule
metadata:
  name: placement-install-lvms
spec:
  clusterConditions:
  - status: "True"
    type: ManagedClusterConditionAvailable
  clusterSelector: <1>
    matchExpressions:
    - key: mykey
      operator: In
      values:
      - myvalue
---
apiVersion: policy.open-cluster-management.io/v1
kind: PlacementBinding
metadata:
  name: binding-install-lvms
placementRef:
  apiGroup: apps.open-cluster-management.io
  kind: PlacementRule
  name: placement-install-lvms
subjects:
- apiGroup: policy.open-cluster-management.io
  kind: Policy
  name: install-lvms
---
apiVersion: policy.open-cluster-management.io/v1
kind: Policy
metadata:
  annotations:
    policy.open-cluster-management.io/categories: CM Configuration Management
    policy.open-cluster-management.io/controls: CM-2 Baseline Configuration
    policy.open-cluster-management.io/standards: NIST SP 800-53
  name: install-lvms
spec:
  disabled: false
  remediationAction: enforce
  policy-templates:
  - objectDefinition:
      apiVersion: policy.open-cluster-management.io/v1
      kind: ConfigurationPolicy
      metadata:
        name: install-lvms
      spec:
        object-templates:
        - complianceType: musthave
          objectDefinition: <2>
            apiVersion: v1
            kind: Namespace
            metadata:
              labels:
                openshift.io/cluster-monitoring: "true"
                pod-security.kubernetes.io/enforce: privileged
                pod-security.kubernetes.io/audit: privileged
                pod-security.kubernetes.io/warn: privileged
              name: openshift-lvm-storage
        - complianceType: musthave
          objectDefinition: <3>
            apiVersion: operators.coreos.com/v1
            kind: OperatorGroup
            metadata:
              name: openshift-storage-operatorgroup
              namespace: openshift-lvm-storage
            spec:
              targetNamespaces:
              - openshift-lvm-storage
        - complianceType: musthave
          objectDefinition: <4>
            apiVersion: operators.coreos.com/v1alpha1
            kind: Subscription
            metadata:
              name: lvms
              namespace: openshift-lvm-storage
            spec:
              installPlanApproval: Automatic
              name: lvms-operator
              source: redhat-operators
              sourceNamespace: openshift-marketplace
        remediationAction: enforce
        severity: low
```
<1> Set the `key` field and `values` field in `PlacementRule.spec.clusterSelector` to match the labels that are configured in the clusters on which you want to install LVM Storage.
<2> Namespace configuration.
<3> The `OperatorGroup` CR configuration.
<4> The `Subscription` CR configuration.

1. Create the `Policy` CR by running the following command:
```bash
$ oc create -f <file_name> -n <namespace>
```
Upon creating the `Policy` CR, the following custom resources are created on the clusters that match the selection criteria configured in the `PlacementRule` CR:

- `Namespace`
- `OperatorGroup`
- `Subscription`

> **NOTE:** The default namespace for the LVM Storage Operator is `openshift-lvm-storage`.
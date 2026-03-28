# Enabling and disabling OADP Self-Service

Enable or disable the OADP Self-Service feature to allow namespace administrators to manage their own backup and restore operations without cluster admin privileges. This helps you delegate backup responsibilities while maintaining administrative control.

> **NOTE:** You can install only one instance of the `NonAdminController` (NAC) CR in the cluster. If you install multiple instances of the NAC CR, you get the following error: [source,terminal] ---- message: only a single instance of Non-Admin Controller can be installed across the entire cluster. Non-Admin controller is already configured and installed in openshift-adp namespace. ----

.Prerequisites

- You are logged in to the cluster with the `cluster-admin` role.
- You have installed the OADP Operator.
- You have configured the DPA.

.Procedure

- To enable OADP Self-Service, edit the DPA CR to configure the `nonAdmin.enable` section. See the following example configuration:
.Example `DataProtectionApplication` CR
```yaml
apiVersion: oadp.openshift.io/v1alpha1
kind: DataProtectionApplication
metadata:
  name: oadp-backup
  namespace: openshift-adp
spec:
  configuration:
    nodeAgent:
      enable: true
      uploaderType: kopia
    velero:
      defaultPlugins:
        - aws
        - openshift
        - csi
      defaultSnapshotMoveData: true
  nonAdmin:
    enable: true
  backupLocations:
    - velero:
        config:
          profile: "default"
          region: noobaa
          s3Url: https://s3.openshift-storage.svc 
          s3ForcePathStyle: "true"
          insecureSkipTLSVerify: "true"
        provider: aws
        default: true
        credential:
          key: cloud
          name:  <cloud_credentials>
        objectStorage:
          bucket: <bucket_name> 
          prefix: oadp  
```
where:
`nonAdmin`:: Specifies the section in the `spec` section of the DPA to enable or disable the Self-Service feature.
`enable`:: Specifies whether to enable the Self-Service feature. Set to `true` to enable the feature. Set to `false` to disable the feature.

.Verification

- To verify that the `NonAdminController` (NAC) pod is running in the OADP namespace, run the following command:
```bash
$ oc get pod -n openshift-adp -l control-plane=non-admin-controller
```
.Example output
```bash
NAME                                  READY   STATUS    RESTARTS   AGE
non-admin-controller-5d....f5-p..9p   1/1     Running   0          99m
```
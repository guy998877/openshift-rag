# Using the DataProtectionTest custom resource

Configure and run the `DataProtectionTest` (DPT) custom resource (CR) to verify Container Storage Interface (CSI) snapshot readiness and data upload performance to your storage bucket. This helps you validate your OADP environment before performing backup and restore operations.

.Prerequisites

- You have logged in to the OpenShift Container Platform cluster as a user with the `cluster-admin` role.
- You have installed the OpenShift CLI (`oc`).
- You have installed the OADP Operator.
- You have created the `DataProtectionApplication` (DPA) CR.
- You have configured a backup storage location (BSL) to store the backups.
- You have an application with persistent volume claims (PVCs) running in a separate namespace.

.Procedure

1.  Create a manifest file for the DPT CR as shown in the example:
```yaml
apiVersion: oadp.openshift.io/v1alpha1
kind: DataProtectionTest
metadata:
  name: dpt-sample
  namespace: openshift-adp
spec:
  backupLocationName: <bsl_name>
  csiVolumeSnapshotTestConfigs:
  - snapshotClassName: csi-gce-pd-vsc
    timeout: 90s
    volumeSnapshotSource:
      persistentVolumeClaimName: <pvc1_name>
      persistentVolumeClaimNamespace: <pvc_namespace>
  - snapshotClassName: csi-gce-pd-vsc
    timeout: 120s
    volumeSnapshotSource:
      persistentVolumeClaimName: <pvc2_name>
      persistentVolumeClaimNamespace: <pvc_namespace>
  forceRun: false
  uploadSpeedTestConfig:
    fileSize: 200MB
    timeout: 120s
```
where:
`<bsl_name>`:: Specifies the name of the BSL.
`csiVolumeSnapshotTestConfigs`:: Specifies a list for `csiVolumeSnapshotTestConfigs`. In this example, two PVCs are being tested.
`<pvc1_name>`:: Specifies the name of the first PVC.
`<pvc_namespace>`:: Specifies the namespace of the PVC.
`<pvc2_name>`:: Specifies the name of the second PVC.
`forceRun`:: Set to `false` if you want to make the OADP controller skip re-running tests.
`uploadSpeedTestConfig`:: Configures the upload speed test by setting the `fileSize` and `timeout` fields.

1. Create the DPT CR by running the following command:
```bash
$ oc create -f <dpt_file_name>
```
Replace `<dpt_file_name>` with the file name of the DPT manifest.

.Verification

1. Verify that the phase of the DPT CR is `Complete` by running the following command:
```bash
$ oc get dpt dpt-sample
```
The example output is as following:
```bash
NAME         PHASE      LASTTESTED   UPLOADSPEED(MBPS)   ENCRYPTION   VERSIONING   SNAPSHOTS    AGE
dpt-sample   Complete   17m          546                 AES256       Enabled      2/2 passed   17m
```

1. Verify that the CSI snapshots are ready and the data upload tests are successful by running the following command:
```bash
$ oc get dpt dpt-sample -o yaml
```
The example output is as following:
```yaml
apiVersion: oadp.openshift.io/v1alpha1
kind: DataProtectionTest
....
status:
  bucketMetadata:
    encryptionAlgorithm: AES256
    versioningStatus: Enabled
  lastTested: "202...:47:51Z"
  phase: Complete
  s3Vendor: AWS
  snapshotSummary: 2/2 passed
  snapshotTests:
  - persistentVolumeClaimName: mysql-data
    persistentVolumeClaimNamespace: ocp-mysql
    readyDuration: 24s
    status: Ready
  - persistentVolumeClaimName: mysql-data1
    persistentVolumeClaimNamespace: ocp-mysql
    readyDuration: 40s
    status: Ready
  uploadTest:
    duration: 3.071s
    speedMbps: 546
    success: true
```
where:
`bucketMetadata`:: Specifies the bucket metadata information.
`s3Vendor`:: Specifies the S3 bucket vendor.
`snapshotSummary`:: Specifies the summary of the CSI snapshot tests.
`uploadTest`:: Specifies the upload test details.
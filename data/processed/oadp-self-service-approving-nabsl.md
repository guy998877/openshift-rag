# Approving a NonAdminBackupStorageLocation request

Approve `NonAdminBackupStorageLocation` (NABSL) custom resource requests from namespace administrators to grant access to their specified backup storage locations. This enables self-service backup and restore operations for namespace resources.

.Prerequisites

- You are logged in to the cluster with the `cluster-admin` role.
- You have installed the OADP Operator.
- You have enabled OADP Self-Service in the `DataProtectionApplication` (DPA) CR.
- You have enabled the NABSL CR approval workflow in the DPA.

.Procedure

1. To see the NABSL CR requests that are in queue for administrator approval, run the following command:
```bash
$ oc -n openshift-adp get NonAdminBackupStorageLocationRequests
```
.Example output
```bash
NAME                          REQUEST-PHASE   REQUEST-NAMESPACE     REQUEST-NAME               AGE
non-admin-bsl-test-.....175   Approved        non-admin-bsl-test    incorrect-bucket-nabsl    4m57s
non-admin-bsl-test-.....196   Approved        non-admin-bsl-test    perfect-nabsl             5m26s
non-admin-bsl-test-s....e1a   Rejected        non-admin-bsl-test    suspicious-sample         2m56s
non-admin-bsl-test-.....5e0   Pending         non-admin-bsl-test    waitingapproval-nabsl     4m20s
```

1. To approve the NABSL CR request, set the `approvalDecision` field to `approve` by running the following command:
```bash
$ oc patch nabslrequest <nabsl_name> -n openshift-adp --type=merge -p '{"spec": {"approvalDecision": "approve"}}'
```
Replace `<nabsl_name>` with the name of the `NonAdminBackupStorageLocationRequest` CR.

.Verification

- Verify that the Velero backup storage location is created and the phase is `Available` by running the following command:
```bash
$ oc get velero.io.backupstoragelocation
```
.Example output

```bash
NAME                         PHASE       LAST VALIDATED   AGE   DEFAULT
test-nac-test-bsl-cd...930   Available   62s              62s   
```
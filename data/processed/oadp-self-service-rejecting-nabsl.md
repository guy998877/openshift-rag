# Rejecting a NonAdminBackupStorageLocation request

Reject `NonAdminBackupStorageLocation` (NABSL) custom resource (CR) requests from namespace administrators to deny access to backup storage locations that do not meet requirements. This helps you maintain security and compliance standards.

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
$ oc get nabslrequest
NAME                          REQUEST-PHASE   REQUEST-NAMESPACE     REQUEST-NAME               AGE
non-admin-bsl-test-.....175   Approved        non-admin-bsl-test    incorrect-bucket-nabsl    4m57s
non-admin-bsl-test-.....196   Approved        non-admin-bsl-test    perfect-nabsl             5m26s
non-admin-bsl-test-s....e1a   Rejected        non-admin-bsl-test    suspicious-sample         2m56s
non-admin-bsl-test-.....5e0   Pending         non-admin-bsl-test    waitingapproval-nabsl     4m20s
```

1. To reject the NABSL CR request, set the `approvalDecision` field to `reject` by running the following command:
```bash
$ oc patch nabslrequest <nabsl_name> -n openshift-adp --type=merge -p '{"spec": {"approvalDecision": "reject"}}'
```
Replace `<nabsl_name>` with the name of the `NonAdminBackupStorageLocationRequest` CR.
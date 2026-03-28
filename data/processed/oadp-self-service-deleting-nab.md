# Deleting a NonAdminBackup CR

As a namespace admin user, you can delete a `NonAdminBackup` (NAB) custom resource (CR).

.Prerequisites

- You are logged in to the cluster as a namespace admin user.
- The cluster administrator has installed the OADP Operator.
- The cluster administrator has configured the `DataProtectionApplication` (DPA) CR to enable OADP Self-Service.
- The cluster administrator has created a namespace for you and has authorized you to operate from that namespace.
- You have created a NAB CR in your authorized namespace.

.Procedure

1. Edit the `NonAdminBackup` CR YAML manifest file by running the following command:
```bash
$ oc edit <nab_cr> -n <authorized_namespace> 
```
where:

`<nab_cr>`:: Specifies the name of the NAB CR to be deleted.
`<authorized_namespace>`:: Specifies the name of your authorized namespace.

1. Update the NAB CR YAML manifest file and add the `deleteBackup` flag as shown in the following example:
```yaml
apiVersion: oadp.openshift.io/v1alpha1
kind: NonAdminBackup
metadata:
  name: <nab_cr>
spec:
  backupSpec:
    includedNamespaces:
    - <authorized_namespace>
    deleteBackup: true
```
where:

`<nab_cr>`:: Specify the name of the NAB CR to be deleted.
`<authorized_namespace>`:: Specify the name of your authorized namespace.
`deleteBackup: true`:: Add the `deleteBackup` flag and set it to `true`.

.Verification

- Verify that the NAB CR is deleted by running the following command:
```bash
$ oc get nab <nab_cr>
```
`<nab_cr>` is the name of the NAB CR you deleted.
You should see an output as shown in the following example:
```bash
Error from server (NotFound): nonadminbackups.oadp.openshift.io "test-nab" not found
```
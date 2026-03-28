// Module included in the following assemblies:
//
// * backup_and_restore/application_backup_and_restore/installing/installing-oadp-kubevirt.adoc

# Restoring a single VM from a backup of multiple VMs

If you have a backup containing multiple virtual machines (VMs), and you want to restore only one VM, you can use the `LabelSelectors` section in the `Restore` CR to select the VM to restore. To ensure that the persistent volume claim (PVC) attached to the VM is correctly restored, and the restored VM is not stuck in a `Provisioning` status, use both the `app: <vm_name>` and the `kubevirt.io/created-by` labels. To match the `kubevirt.io/created-by` label, use the UID of `DataVolume` of the VM.

.Prerequisites

- You have installed the OADP Operator.
- You have labeled the VMs that need to be backed up.
- You have a backup of multiple VMs.

.Procedure

1. Before you take a backup of many VMs, ensure that the VMs are labeled by running the following command:
```bash
$ oc label vm <vm_name> app=<vm_name> -n openshift-adp 
```

1. Configure the label selectors in the `Restore` CR as shown in the following example:
.Example `Restore` CR
```yaml
apiVersion: velero.io/v1
kind: Restore
metadata:
  name: singlevmrestore
  namespace: openshift-adp
spec:
  backupName: multiplevmbackup
  restorePVs: true
  LabelSelectors:
    - matchLabels:
        kubevirt.io/created-by: <datavolume_uid>
    - matchLabels:
        app: <vm_name>
```
where:
`datavolume_uid`:: Specifies the UID of `DataVolume` of the VM that you want to restore. For example, `b6...53a-ddd7-4d9d-9407-a0c...e5`.
`vm_name`:: Specifies the name of the VM that you want to restore. For example, `test-vm`.

1. To restore a VM, run the following command:
```bash
$ oc apply -f <restore_cr_file_name>
```
where:
`restore_cr_file_name`:: Specifies the name of the `Restore` CR file.
// end of module. Need to add this comment because the level offset attribute does not get unset at the end of this module due to the continuation plus symbol. Causing the level offset from this module to stack on to the next module. This causes build failures or deeply nested modules.
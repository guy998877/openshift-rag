# Troubleshooting Restic permission errors for NFS data volumes

Create a supplemental group and add its group ID to the `DataProtectionApplication` customer resource CR to resolve `Restic` permission errors on NFS data volumes with `root_squash` enabled. This helps you to restore backup functionality for NFS volumes without disabling root squash.

If your NFS data volumes have the `root_squash` parameter enabled, `Restic` maps set to the `nfsnobody` value, and do not have permission to create backups, the `Restic` pod log displays the following error message:

```text
controller=pod-volume-backup error="fork/exec/usr/bin/restic: permission denied".
```

.Procedure

1. Create a supplemental group for `Restic` on the NFS data volume.

1. Set the `setgid` bit on the NFS directories so that group ownership is inherited.

1. Add the `spec.configuration.nodeAgent.supplementalGroups` parameter and the group ID to the `DataProtectionApplication` manifest, as shown in the following example:
```yaml
apiVersion: oadp.openshift.io/v1alpha1
kind: DataProtectionApplication
# ...
spec:
  configuration:
    nodeAgent:
      enable: true
      uploaderType: restic
      supplementalGroups:
      - <group_id>
# ...
```
where:
`<group_id>`:: Specifies the supplemental group ID.

1. Wait for the `Restic` pods to restart so that the changes are applied.
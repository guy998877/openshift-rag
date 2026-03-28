# Pruning groups

To prune groups records from an external provider, administrators can run the
following command:

```bash
$ oc adm prune groups \
    --sync-config=path/to/sync/config [<options>]
```

.`oc adm prune groups` flags
[cols="4,8",options="header"]
|===

|Options |Description

.^|`--confirm`
|Indicate that pruning should occur, instead of performing a dry-run.

.^|`--blacklist`
|Path to the group blacklist file.

.^|`--whitelist`
|Path to the group whitelist file.

.^|`--sync-config`
|Path to the synchronization configuration file.
|===

.Procedure

1. To see the groups that the prune command deletes, run the following command:
```bash
$ oc adm prune groups --sync-config=ldap-sync-config.yaml
```

1. To perform the prune operation, add the `--confirm` flag:
```bash
$ oc adm prune groups --sync-config=ldap-sync-config.yaml --confirm
```

////
Needs "Additional resources" links when converted:

//Future Configuring LDAP Sync
//Future Syncing Groups With LDAP
////
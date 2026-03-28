# Syncing OpenShift Container Platform groups with the LDAP server

You can sync all groups already in OpenShift Container Platform that correspond to groups in the
LDAP server specified in the configuration file.

.Prerequisites

- Create a sync configuration file.
- You have access to the cluster as a user with the `cluster-admin` role.

.Procedure

- To sync OpenShift Container Platform groups with the LDAP server:
```bash
$ oc adm groups sync --type=openshift --sync-config=config.yaml --confirm
```
> **NOTE:** By default, all group synchronization operations are dry-run, so you must set the `--confirm` flag on the `oc adm groups sync` command to make changes to OpenShift Container Platform group records.
# Syncing subgroups from the LDAP server with OpenShift Container Platform

You can sync a subset of LDAP groups with OpenShift Container Platform using whitelist files,
blacklist files, or both.

> **NOTE:** You can use any combination of blacklist files, whitelist files, or whitelist literals. Whitelist and blacklist files must contain one unique group identifier per line, and you can include whitelist literals directly in the command itself. These guidelines apply to groups found on LDAP servers as well as groups already present in OpenShift Container Platform.

.Prerequisites

- Create a sync configuration file.
- You have access to the cluster as a user with the `cluster-admin` role.

.Procedure

- To sync a subset of LDAP groups with OpenShift Container Platform, use any the following commands:
```bash
$ oc adm groups sync --whitelist=<whitelist_file> \
                   --sync-config=config.yaml      \
                   --confirm
```
```bash
$ oc adm groups sync --blacklist=<blacklist_file> \
                   --sync-config=config.yaml      \
                   --confirm
```
```bash
$ oc adm groups sync <group_unique_identifier>    \
                   --sync-config=config.yaml      \
                   --confirm
```
```bash
$ oc adm groups sync <group_unique_identifier>  \
                   --whitelist=<whitelist_file> \
                   --blacklist=<blacklist_file> \
                   --sync-config=config.yaml    \
                   --confirm
```
```bash
$ oc adm groups sync --type=openshift           \
                   --whitelist=<whitelist_file> \
                   --sync-config=config.yaml    \
                   --confirm
```
> **NOTE:** By default, all group synchronization operations are dry-run, so you must set the `--confirm` flag on the `oc adm groups sync` command to make changes to OpenShift Container Platform group records.
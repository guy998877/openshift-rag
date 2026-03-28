# Backing up the DPA configuration

You must back up your current `DataProtectionApplication` (DPA) configuration.

.Procedure

- Save your current DPA configuration by running the following command:
.Example command
```bash
$ oc get dpa -n openshift-adp -o yaml > dpa.orig.backup
```
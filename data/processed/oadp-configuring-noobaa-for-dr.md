# Configuring Multicloud Object Gateway (MCG) for disaster recovery on OpenShift Data Foundation

If you use cluster storage for your MCG bucket `backupStorageLocation` on OpenShift Data Foundation, configure MCG as an external object store.

> **WARNING:** Failure to configure MCG as an external object store might lead to backups not being available.

.Procedure

- Configure MCG as an external object store as described in link:https://access.redhat.com/documentation/en-us/red_hat_openshift_data_foundation/4.13/html/managing_hybrid_and_multicloud_resources/adding-storage-resources-for-hybrid-or-multicloud_rhodf#doc-wrapper[Adding storage resources for hybrid or Multicloud].
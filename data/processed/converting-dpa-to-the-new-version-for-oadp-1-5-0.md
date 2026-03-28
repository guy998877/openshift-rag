# Converting DPA to the new version for OADP 1.5.0

The OpenShift API for Data Protection (OADP) 1.4 is not supported on {OCP-short} 4.19. You can convert Data Protection Application (DPA) to the new OADP 1.5 version by using the new `spec.configuration.nodeAgent` field and its sub-fields.

.Procedure

1. To configure `nodeAgent` daemon set, use the `spec.configuration.nodeAgent` parameter in DPA. See the following example:
.Example `DataProtectionApplication` configuration
```yaml
...
 spec:
   configuration:
     nodeAgent:
       enable: true
       uploaderType: kopia
...
```

1. To configure `nodeAgent` daemon set by using the `ConfigMap` resource named `node-agent-config`, see the following example configuration:
.Example config map
```yaml
...
 spec:
   configuration:
     nodeAgent:
       backupPVC:
         ...
       loadConcurrency:
         ...
       podResources:
         ...
       restorePVC:
        ...
...
```
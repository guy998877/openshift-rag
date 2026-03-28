# Implementing item operation timeout - restore

Configure the `ItemOperationTimeout` parameter in the `Restore` custom resource (CR) to define how long restore operations wait to complete. Adjusting this timeout prevents failures when Data Mover needs more time to download large storage volumes. The default value is `1h`.

.Procedure

- Edit the values in the `Restore.spec.itemOperationTimeout` block of the `Restore` CR manifest, as shown in the following example:
```yaml
apiVersion: velero.io/v1
kind: Restore
metadata:
 name: <restore_name>
spec:
 itemOperationTimeout: 1h
# ...
```
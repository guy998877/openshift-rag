# Configuring journald settings

If you need to configure settings for the `journald` service on OpenShift Container Platform nodes, you can do that by modifying the appropriate configuration file and passing the file to the appropriate pool of nodes as a machine config.

This procedure describes how to modify `journald` rate limiting settings in the `/etc/systemd/journald.conf` file and apply them to worker nodes. See the `journald.conf` man page for information on how to use that file.

.Prerequisites
- Have a running OpenShift Container Platform cluster.
- Log in to the cluster as a user with administrative privileges.

.Procedure

1. Create a Butane config file, `40-worker-custom-journald.bu`, that includes an `/etc/systemd/journald.conf` file with the required settings.
> **NOTE:** include::snippets/butane-version.adoc[]
```yaml
variant: openshift
version: 4.21.0
metadata:
  name: 40-worker-custom-journald
  labels:
    machineconfiguration.openshift.io/role: worker
storage:
  files:
  - path: /etc/systemd/journald.conf
    mode: 0644
    overwrite: true
    contents:
      inline: |
        # Disable rate limiting
        RateLimitInterval=1s
        RateLimitBurst=10000
        Storage=volatile
        Compress=no
        MaxRetentionSec=30s
```

1. Use Butane to generate a `MachineConfig` object file, `40-worker-custom-journald.yaml`, containing the configuration to be delivered to the worker nodes:
```bash
$ butane 40-worker-custom-journald.bu -o 40-worker-custom-journald.yaml
```

1. Apply the machine config to the pool:
```bash
$ oc apply -f 40-worker-custom-journald.yaml
```

1. Check that the new machine config is applied and that the nodes are not in a degraded state. It might take a few minutes. The worker pool will show the updates in progress, as each node successfully has the new machine config applied:
```bash
$ oc get machineconfigpool
```
.Example output
```bash
NAME   CONFIG             UPDATED UPDATING DEGRADED MACHINECOUNT READYMACHINECOUNT UPDATEDMACHINECOUNT DEGRADEDMACHINECOUNT AGE
master rendered-master-35 True    False    False    3            3                 3                   0                    34m
worker rendered-worker-d8 False   True     False    3            1                 1                   0                    34m
```

1. To check that the change was applied, you can log in to a worker node:
```bash
$ oc get node | grep worker
```
.Example output
```bash
ip-10-0-0-1.us-east-2.compute.internal   Ready    worker   39m   v0.0.0-master+$Format:%h$
```
```bash
$ oc debug node/ip-10-0-0-1.us-east-2.compute.internal
```
.Example output
```bash
Starting pod/ip-10-0-141-142us-east-2computeinternal-debug ...
...
sh-4.2# chroot /host
sh-4.4# cat /etc/systemd/journald.conf
# Disable rate limiting
RateLimitInterval=1s
RateLimitBurst=10000
Storage=volatile
Compress=no
MaxRetentionSec=30s
sh-4.4# exit
```
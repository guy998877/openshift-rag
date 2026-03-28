[id=storage-ephemeral-storage-monitoring_{context}]
# Monitoring ephemeral storage

To monitor ephemeral storage usage, use the `/bin/df` utility. By using this tool, you can track disk space consumption on the volumes where ephemeral container data resides, specifically `/var/lib/kubelet` and `/var/lib/containers`.

When you use the `df` command, the available space for only `/var/lib/kubelet` is shown if `/var/lib/containers` is placed on a separate disk by the cluster administrator.

.Procedure

- To show the human-readable values of used and available space in `/var/lib`, enter the following command:
```bash
$ df -h /var/lib
```
The output shows the ephemeral storage usage in `/var/lib`:
.Example output
```bash
Filesystem  Size  Used Avail Use% Mounted on
/dev/disk/by-partuuid/4cd1448a-01    69G   32G   34G  49% /
```
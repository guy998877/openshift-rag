# Downloading log files and diagnostic information using must-gather

When LVM Storage is unable to automatically resolve a problem, use the must-gather tool to collect the log files and diagnostic information so that you or the Red Hat Support can review the problem and determine a solution.

.Procedure
- Run the `must-gather` command from the client connected to the LVM Storage cluster:
```bash
$ oc adm must-gather --image=registry.redhat.io/lvms4/lvms-must-gather-rhel9:v4.21 --dest-dir=<directory_name>
```
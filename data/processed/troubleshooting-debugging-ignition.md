# Debugging Ignition failures

If a machine cannot be provisioned, Ignition fails and RHCOS will boot into the emergency shell. Use the following procedure to get debugging information.

.Procedure

1. Run the following command to show which service units failed:
```bash
$ systemctl --failed
```

1. Optional: Run the following command on an individual service unit to find out more information:
```bash
$ journalctl -u <unit>.service
```
# Connecting to a pod

You can directly connect to a currently running pod with the `oc rsh` command, which provides you with a shell on that pod.

> **WARNING:** In pods that run a low-latency application, latency issues can occur when you run the `oc rsh` command. Use the `oc rsh` command only if you cannot connect to the node by using the `oc debug` command.

.Procedure

- Connect to your pod by running the following command:
```bash
$ oc rsh -n <namespace> busybox-1
```

For more information, see "oc rsh" and "Accessing running pods".
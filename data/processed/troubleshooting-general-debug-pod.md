# Debugging a pod

In certain cases, you do not want to directly interact with your pod that is in production.

To avoid interfering with running traffic, you can use a secondary pod that is a copy of your original pod.
The secondary pod uses the same components as that of the original pod but does not have running traffic.

.Procedure

1. List the pods by running the following command:
--
```bash
$ oc get pod
```

.Example output
```bash
NAME        READY   STATUS    RESTARTS          AGE
busybox-1   1/1     Running   168 (34m ago)     7d
busybox-2   1/1     Running   119 (9m20s ago)   4d23h
busybox-3   1/1     Running   168 (43m ago)     7d
busybox-4   1/1     Running   168 (43m ago)     7d
```
--

1. Debug a pod by running the following command: 
--
```bash
$ oc debug -n <namespace> busybox-1
```

.Example output
```bash
Starting pod/busybox-1-debug, command was: sleep 3600
Pod IP: 10.133.2.11
```

If you do not see a shell prompt, press Enter.
--

For more information, see "oc debug" and "Starting debug pods with root access".
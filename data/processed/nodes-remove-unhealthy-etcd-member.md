# Removing the unhealthy etcd member

Begin removing the failed control plane node by first removing the unhealthy etcd member.

.Procedure

1. List etcd pods by running the following command and make note of a pod that is not on the affected node:
```bash
$ oc -n openshift-etcd get pods -l k8s-app=etcd -o wide
```
.Example output
```bash
etcd-openshift-control-plane-0   5/5   Running   11   3h56m   192.168.10.9    openshift-control-plane-0  <none>           <none>
etcd-openshift-control-plane-1   5/5   Running   0    3h54m   192.168.10.10   openshift-control-plane-1   <none>           <none>
etcd-openshift-control-plane-2   5/5   Running   0    3h58m   192.168.10.11   openshift-control-plane-2   <none>           <none>
```

1. Connect to a running etcd container by running the following command:
```bash
$ oc rsh -n openshift-etcd <etcd_pod>
```
Replace `<etcd_pod>` with the name of an etcd pod associated with one of the healthy nodes.
.Example command
```bash
$ oc rsh -n openshift-etcd etcd-openshift-control-plane-0
```

1. View the etcd member list by running the following command. Make note of the ID and the name of the unhealthy etcd member because these values are required later.
```bash
sh-4.2# etcdctl member list -w table
```
.Example output
```bash
+------------------+---------+------------------------------+---------------------------+---------------------------+
|        ID        | STATUS  |             NAME             |        PEER ADDRS         |       CLIENT ADDRS        |
+------------------+---------+------------------------------+---------------------------+---------------------------+
| 6fc1e7c9db35841d | started | openshift-control-plane-2    | https://10.0.131.183:2380 | https://10.0.131.183:2379 |
| 757b6793e2408b6c | started | openshift-control-plane-1    | https://10.0.164.97:2380  | https://10.0.164.97:2379  |
| ca8c2990a0aa29d1 | started | openshift-control-plane-0    | https://10.0.154.204:2380 | https://10.0.154.204:2379 |
+------------------+---------+------------------------------+---------------------------+---------------------------+
```
> **IMPORTANT:** The `etcdctl endpoint health` command will list the removed member until the replacement is complete and the new member is added.

1. Remove the unhealthy etcd member by running the following command:
```bash
sh-4.2# etcdctl member remove <unhealthy_member_id>
```
Replace `<unhealthy_member_id>` with the ID of the etcd member on the unhealthy node.
.Example command
```bash
sh-4.2# etcdctl member remove 6fc1e7c9db35841d
```
.Example output
```bash
Member 6fc1e7c9db35841d removed from cluster b23536c33f2cdd1b
```

1. View the member list again by running the following command and verify that the member was removed:
```bash
sh-4.2# etcdctl member list -w table
```
.Example output
```bash
+------------------+---------+------------------------------+---------------------------+---------------------------+
|        ID        | STATUS  |             NAME             |        PEER ADDRS         |       CLIENT ADDRS        |
+------------------+---------+------------------------------+---------------------------+---------------------------+
| 757b6793e2408b6c | started | openshift-control-plane-1    | https://10.0.164.97:2380  | https://10.0.164.97:2379  |
| ca8c2990a0aa29d1 | started | openshift-control-plane-0    | https://10.0.154.204:2380 | https://10.0.154.204:2379 |
+------------------+---------+------------------------------+---------------------------+---------------------------+
```
> **IMPORTANT:** After you remove the member, the cluster might be unreachable for a short time while the remaining etcd instances reboot.

1. Exit the rsh session into the etcd pod by running the following command:
```bash
sh-4.2# exit
```

1. Turn off the etcd quorum guard by running the following command:
```bash
$ oc patch etcd/cluster --type=merge -p '{"spec": {"unsupportedConfigOverrides": {"useUnsupportedUnsafeNonHANonProductionUnstableEtcd": true}}}'
```
This command ensures that you can successfully re-create secrets and roll out the static pods.

1. List the secrets for the removed, unhealthy etcd member by running the following command:
```bash
$ oc get secrets -n openshift-etcd | grep <node_name>
```
Replace `<node_name>` with the name of the failed node whose etcd member you removed.
.Example command
```bash
$ oc get secrets -n openshift-etcd | grep openshift-control-plane-2
```
.Example output
```bash
etcd-peer-openshift-control-plane-2             kubernetes.io/tls   2   134m
etcd-serving-metrics-openshift-control-plane-2  kubernetes.io/tls   2   134m
etcd-serving-openshift-control-plane-2          kubernetes.io/tls   2   134m
```

1. Delete the secrets associated with the affected node that was removed:

.. Delete the peer secret by running the following command:
```bash
$ oc delete secret -n openshift-etcd etcd-peer-<node_name>
```
Replace `<node_name>` with the name of the affected node.

.. Delete the serving secret by running the following command:
```bash
$ oc delete secret -n openshift-etcd etcd-serving-<node_name>
```
Replace `<node_name>` with the name of the affected node.

.. Delete the metrics secret by running the following command:
```bash
$ oc delete secret -n openshift-etcd etcd-serving-metrics-<node_name> <1>
```
Replace `<node_name>` with the name of the affected node.
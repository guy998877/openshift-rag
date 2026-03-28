# Adding the new etcd member

Finish adding the new control plane node by adding the new etcd member to the cluster.

.Procedure

1. Add the new etcd member to the cluster by performing the following steps in a single bash shell session:

.. Find the IP of the new control plane node by running the following command:
```bash
$ oc get nodes -owide -l node-role.kubernetes.io/control-plane
```
Make note of the node's IP address for later use.

.. List the etcd pods by running the following command:
```bash
$ oc get -n openshift-etcd pods -l k8s-app=etcd -o wide
```

.. Connect to one of the running etcd pods by running the following command. The etcd pod on the new node should be in a `CrashLoopBackOff` state.
```bash
$ oc rsh -n openshift-etcd <running_pod>
```
Replace `<running_pod>` with the name of a running pod shown in the previous step.

.. View the etcd member list by running the following command:
```bash
sh-4.2# etcdctl member list -w table
```

.. Add the new control plane etcd member by running the following command:
```bash
sh-4.2# etcdctl member add <new_node> --peer-urls="https://<ip_address>:2380"
```
where:

`<new_node>`:: Specifies the name of the new control plane node
`<ip_address>`:: Specifies the IP address of the new node.

.. Exit the rsh shell by running the following command:
```bash
sh-4.2# exit
```

1. Force an etcd redeployment by running the following command:
```bash
$ oc patch etcd cluster -p='{"spec": {"forceRedeploymentReason": "single-master-recovery-'"$( date --rfc-3339=ns )"'"}}' --type=merge
```

1. Turn the etcd quorum guard back on by running the following command:
```bash
$ oc patch etcd/cluster --type=merge -p '{"spec": {"unsupportedConfigOverrides": null}}'
```

1. Monitor the cluster Operator rollout by running the following command:
```bash
$ watch oc get co
```
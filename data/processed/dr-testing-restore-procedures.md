# Testing restore procedures

Testing the restore procedure is important to ensure that your automation and workload handle the new cluster state gracefully. Due to the complex nature of etcd quorum and the etcd Operator attempting to mend automatically, it is often difficult to correctly bring your cluster into a broken enough state that it can be restored.

> **WARNING:** You **must** have SSH access to the cluster. Your cluster might be entirely lost without SSH access.

.Prerequisites

- You have SSH access to control plane hosts.
- You have installed the pass:quotes[OpenShift CLI (`oc`)].

.Procedure

1. Use SSH to connect to each of your nonrecovery nodes and run the following commands to disable etcd and the `kubelet` service:

.. Disable etcd by running the following command:
```bash
$ sudo /usr/local/bin/disable-etcd.sh
```

.. Delete variable data for etcd by running the following command:
```bash
$ sudo rm -rf /var/lib/etcd
```

.. Disable the `kubelet` service by running the following command:
```bash
$ sudo systemctl disable kubelet.service
```

1. Exit every SSH session.

1. Run the following command to ensure that your nonrecovery nodes are in a `NOT READY` state:
```bash
$ oc get nodes
```

1. Follow the steps in "Restoring to a previous cluster state" to restore your cluster.

1. After you restore the cluster and the API responds, use SSH to connect to each nonrecovery node and enable the `kubelet` service:
```bash
$ sudo systemctl enable kubelet.service
```

1. Exit every SSH session.

1. Run the following command to observe your nodes coming back into the `READY` state:
```bash
$ oc get nodes
```

1. Run the following command to verify that etcd is available:
```bash
$ oc get pods -n openshift-etcd
```
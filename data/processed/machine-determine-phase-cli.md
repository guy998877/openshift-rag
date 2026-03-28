# Determining the phase of a machine by using the CLI

You can find the phase of a machine by using the OpenShift CLI (`oc`).

.Prerequisites

- You have access to an OpenShift Container Platform cluster using an account with `cluster-admin` permissions.
- You have installed the `oc` CLI.

.Procedure

- List the machines on the cluster by running the following command:
```bash
$ oc get machine -n openshift-machine-api
```
.Example output
```text
NAME                                      PHASE     TYPE         REGION      ZONE         AGE
mycluster-5kbsp-master-0                  Running   m6i.xlarge   us-west-1   us-west-1a   4h55m
mycluster-5kbsp-master-1                  Running   m6i.xlarge   us-west-1   us-west-1b   4h55m
mycluster-5kbsp-master-2                  Running   m6i.xlarge   us-west-1   us-west-1a   4h55m
mycluster-5kbsp-worker-us-west-1a-fmx8t   Running   m6i.xlarge   us-west-1   us-west-1a   4h51m
mycluster-5kbsp-worker-us-west-1a-m889l   Running   m6i.xlarge   us-west-1   us-west-1a   4h51m
mycluster-5kbsp-worker-us-west-1b-c8qzm   Running   m6i.xlarge   us-west-1   us-west-1b   4h51m
```
The `PHASE` column of the output contains the phase of each machine.
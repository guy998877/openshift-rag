# Gathering ClusterVersion history using the pass:quotes[OpenShift CLI (`oc`)]

You can view the ClusterVersion history using the OpenShift CLI (`oc`).

.Prerequisites
- You have access to the cluster as a user with the `cluster-admin` role.
- You have installed the pass:quotes[OpenShift CLI (`oc`)].

.Procedure

1. View the cluster update history by entering the following command:
```bash
$ oc describe clusterversions/version
```
.Example output
```bash
  Desired:
    Channels:
      candidate-4.13
      candidate-4.14
      fast-4.13
      fast-4.14
      stable-4.13
    Image:    quay.io/openshift-release-dev/ocp-release@sha256:a148b19231e4634196717c3597001b7d0af91bf3a887c03c444f59d9582864f4
    URL:      https://access.redhat.com/errata/RHSA-2023:6130
    Version:  4.13.19
  History:
    Completion Time:    2023-11-07T20:26:04Z
    Image:              quay.io/openshift-release-dev/ocp-release@sha256:a148b19231e4634196717c3597001b7d0af91bf3a887c03c444f59d9582864f4
    Started Time:       2023-11-07T19:11:36Z
    State:              Completed
    Verified:           true
    Version:            4.13.19
    Completion Time:    2023-10-04T18:53:29Z
    Image:              quay.io/openshift-release-dev/ocp-release@sha256:eac141144d2ecd6cf27d24efe9209358ba516da22becc5f0abc199d25a9cfcec
    Started Time:       2023-10-04T17:26:31Z
    State:              Completed
    Verified:           true
    Version:            4.13.13
    Completion Time:    2023-09-26T14:21:43Z
    Image:              quay.io/openshift-release-dev/ocp-release@sha256:371328736411972e9640a9b24a07be0af16880863e1c1ab8b013f9984b4ef727
    Started Time:       2023-09-26T14:02:33Z
    State:              Completed
    Verified:           false
    Version:            4.13.12
  Observed Generation:  4
  Version Hash:         CMLl3sLq-EA=
Events:                 <none>
```
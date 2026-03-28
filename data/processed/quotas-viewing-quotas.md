# Viewing a quota

You can view usage statistics related to any hard limits defined in a quota for a project by navigating in the web console to the project's *Quota* page.

You can also use the CLI to view quota details.

.Procedure

1. Get the list of quotas defined in the project. For example, for a project called
`demoproject`:
```bash
$ oc get quota -n demoproject
```
.Example output
```bash
NAME                           AGE    REQUEST                                                                                                      LIMIT
besteffort                     4s     pods: 1/2
compute-resources-time-bound   10m    pods: 0/2                                                                                                    limits.cpu: 0/1, limits.memory: 0/1Gi
core-object-counts             109s   configmaps: 2/10, persistentvolumeclaims: 1/4, replicationcontrollers: 1/20, secrets: 9/10, services: 2/10
```

1. Describe the quota you are interested in, for example the `core-object-counts`
quota:
```bash
$ oc describe quota core-object-counts -n demoproject
```
.Example output
```bash
Name:			core-object-counts
Namespace:		demoproject
Resource		Used	Hard
--------		----	----
configmaps		3	10
persistentvolumeclaims	0	4
replicationcontrollers	3	20
secrets			9	10
services		2	10
```
# Creating object count quotas

You can create an object count quota for all standard namespaced resource types on OpenShift Container Platform, such as `BuildConfig` and `DeploymentConfig` objects. An object quota count places a defined quota on all standard namespaced resource types.

When using a resource quota, an object is charged against the quota upon creation. These types of quotas are useful to protect against exhaustion of resources. The quota can only be created if there are enough spare resources within the project.

.Procedure

To configure an object count quota for a resource:

1. Run the following command:
```bash
$ oc create quota <name> \
    --hard=count/<resource>.<group>=<quota>,count/<resource>.<group>=<quota> <1>
```
<1> The `<resource>` variable is the name of the resource, and `<group>` is the API group, if applicable. Use the `oc api-resources` command for a list of resources and their associated API groups.
For example:
```bash
$ oc create quota test \
    --hard=count/deployments.apps=2,count/replicasets.apps=4,count/pods=3,count/secrets=4
```
.Example output
```bash
resourcequota "test" created
```
This example limits the listed resources to the hard limit in each project in the cluster.

1. Verify that the quota was created:
```bash
$ oc describe quota test
```
.Example output
```bash
Name:                         test
Namespace:                    quota
Resource                      Used  Hard
--------                      ----  ----
count/deployments.apps        0     2
count/pods                    0     3
count/replicasets.apps        0     4
count/secrets                 0     4
```
# Updating a cluster by using the CLI

You can use the OpenShift CLI (`oc`) to review and request cluster updates.

You can find information about available OpenShift Container Platform advisories and updates
[in the errata section](https://access.redhat.com/downloads/content/290)
of the Customer Portal.

.Prerequisites

- You installed the pass:quotes[OpenShift CLI (`oc`)] that matches the version for your updated version.
- You are logged in to the cluster as user with `cluster-admin` privileges.
- You have paused all `MachineHealthCheck` resources.
// Example output Failing=true taken from https://github.com/openshift/oc/blob/main/pkg/cli/admin/upgrade/recommend/examples/4.16.27-degraded-monitoring.output

.Procedure

1. View the available updates and note the version number of the update that you want to apply by running the following command:
```bash
$ oc adm upgrade recommend
```
.Example output
```bash
Failing=True:

  Reason: ClusterOperatorNotAvailable
  Message: Cluster operator monitoring is not available
...
Upstream update service: https://api.integration.openshift.com/api/upgrades_info/graph
Channel: candidate-4.16 (available channels: candidate-4.16, candidate-4.17, candidate-4.18, eus-4.16, fast-4.16, fast-4.17, stable-4.16, stable-4.17)

Updates to 4.16:
  VERSION     ISSUES
  4.16.32     no known issues relevant to this cluster
  4.16.30     no known issues relevant to this cluster
And 2 older 4.16 updates you can see with '--show-outdated-releases' or '--version VERSION'.
```
> **NOTE:** * You can use the `--version` flag to determine whether a specific version is recommended for your update. If there are no recommended updates, updates that have known issues might still be available. * For details and information on how to perform a _Control Plane Only_ update, see "Performing a Control Plane Only update".

1. Based on your organization requirements, set the appropriate update channel by running the following command. For example, you can set your channel to `stable-4.13` or `fast-4.13`. For more information about channels, see "Understanding update channels and releases".
// In OKD, no need to set the channel.
//this example will need to be updated per eus release to reflect options available
```bash
$ oc adm upgrade channel <channel>
```
.Example command
```bash
$ oc adm upgrade channel stable-4.21
```
> **IMPORTANT:** For production clusters, you must subscribe to a `stable-\*`, `eus-*`, or `fast-*` channel.
> **NOTE:** When you are ready to move to the next minor version, choose the channel that corresponds to that minor version. The sooner you declare the update channel, the more effectively the cluster can recommend update paths to your target version. The cluster might take some time to evaluate all the possible updates that are available and offer the best update recommendations to choose from. Update recommendations can change over time, as they are based on what update options are available at the time. If you cannot see an update path to your target minor version, keep updating your cluster to the latest patch release for your current version until the next minor version is available in the path.

1. Apply an update:
- To update to the latest version, run the following command:
```bash
$ oc adm upgrade --to-latest=true
```

- To update to a specific version, run the following command:
```bash
$ oc adm upgrade --to=<version>
```
Replace `<version>` with the update version that you obtained from the output of the `oc adm upgrade recommend` command.
> **IMPORTANT:** When using the `oc adm upgrade --help` command, there is a listed option for the `--force` flag. This is _heavily discouraged_, because using the `--force` option bypasses cluster-side guards, including release verification and precondition checks. Using the `--force` flag does not guarantee a successful update. Bypassing guards puts the cluster at risk.

1. If the cluster administrator evaluates the potential known risks and decides it is acceptable for the current cluster, then the administrator can waive the safety guards and proceed with the update by running the following command:
```bash
$ oc adm upgrade --allow-not-recommended --to <version>
```

1. Optional: Review the status of the Cluster Version Operator by running the following command:
```bash
$ oc adm upgrade status
```
> **NOTE:** To monitor the update in real time, run `oc adm upgrade status` in a `watch` utility.

1. After the update completes, confirm that the cluster version has
updated to the new version by running the following command:
```bash
$ oc adm upgrade
```
.Example output
```bash
Cluster version is <version>

Upstream is unset, so the cluster will use an appropriate default.
Channel: stable-<version> (available channels: candidate-<version>, eus-<version>, fast-<version>, stable-<version>)

No updates available. You may force an update to a specific release image, but doing so might not be supported and might result in downtime or data loss.
```
1. If you are updating your cluster to the next minor version, such as version X.y to X.(y+1), confirm that your nodes are updated before deploying workloads that rely on a new feature. Run the following command:
```bash
$ oc get nodes
```
.Example output
```bash
NAME                           STATUS   ROLES    AGE   VERSION
ip-10-0-168-251.ec2.internal   Ready    master   82m   v1.34.2
ip-10-0-170-223.ec2.internal   Ready    master   82m   v1.34.2
ip-10-0-179-95.ec2.internal    Ready    worker   70m   v1.34.2
ip-10-0-182-134.ec2.internal   Ready    worker   70m   v1.34.2
ip-10-0-211-16.ec2.internal    Ready    master   82m   v1.34.2
ip-10-0-250-100.ec2.internal   Ready    worker   69m   v1.34.2
```
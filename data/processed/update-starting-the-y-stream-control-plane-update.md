# Starting the y-stream control plane update

After you have determined the full new release that you are moving to, you can run the `oc adm upgrade –to=x.y.z` command.

.Procedure
- Start the y-stream control plane update.
For example, run the following command:
```console
$ oc adm upgrade --to=4.16.14
```
.Example output
```console
Requested update to 4.16.14
```
You might move to a z-stream release that has potential issues with platforms other than the one you are running on.
The following example shows a potential problem for cluster updates on Microsoft Azure:
```console
$ oc adm upgrade --to=4.16.15
```
.Example output
```console
error: the update 4.16.15 is not one of the recommended updates, but is available as a conditional update. To accept the Recommended=Unknown risk and to proceed with update use --allow-not-recommended.
  Reason: EvaluationFailed
  Message: Exposure to AzureRegistryImagePreservation is unknown due to an evaluation failure: invalid PromQL result length must be one, but is 0
  In Azure clusters, the in-cluster image registry may fail to preserve images on update. https://issues.redhat.com/browse/IR-461
```
> **NOTE:** The example shows a potential error that can affect clusters hosted in Microsoft Azure. It does not show risks for bare-metal clusters.
```console
$ oc adm upgrade --to=4.16.15 --allow-not-recommended
```
.Example output
```console
warning: with --allow-not-recommended you have accepted the risks with 4.14.11 and bypassed Recommended=Unknown EvaluationFailed: Exposure to AzureRegistryImagePreservation is unknown due to an evaluation failure: invalid PromQL result length must be one, but is 0
In Azure clusters, the in-cluster image registry may fail to preserve images on update. https://issues.redhat.com/browse/IR-461

Requested update to 4.16.15
```
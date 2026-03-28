# About performing a canary rollout update

The following steps outline the high-level workflow of the canary rollout update process:

1. Create custom machine config pools (MCP) based on the worker pool.
> **NOTE:** You can change the `maxUnavailable` setting in an MCP to specify the percentage or the number of machines that can be updating at any given time. The default is `1`.
> **WARNING:** The default setting for `maxUnavailable` is `1` for all the machine config pools in OpenShift Container Platform. It is recommended to not change this value and update one control plane node at a time. Do not change this value to `3` for the control plane pool.

1. Add a node selector to the custom MCPs. For each node that you do not want to update simultaneously with the rest of the cluster, add a matching label to the nodes. This label associates the node to the MCP.
> **IMPORTANT:** Do not remove the default worker label from the nodes. The nodes must have a role label to function properly in the cluster.

1. Pause the MCPs you do not want to update as part of the update process.

1. Perform the cluster update. The update process updates the MCPs that are not paused, including the control plane nodes.

1. Test your applications on the updated nodes to ensure they are working as expected.

1. Unpause one of the remaining MCPs, wait for the nodes in that pool to finish updating, and test the applications on those nodes.
Repeat this process until all worker nodes are updated.

1. Optional: Remove the custom label from updated nodes and delete the custom MCPs.
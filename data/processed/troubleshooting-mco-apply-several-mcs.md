# Applying several machine config files at the same time

When you need to change the machine config for a group of nodes in the cluster, also known as machine config pools (MCPs), sometimes the changes must be applied with several different machine config files.
The nodes need to restart for the machine config file to be applied.
After each machine config file is applied to the cluster, all nodes restart that are affected by the machine config file.

To prevent the nodes from restarting for each machine config file, you can apply all of the changes at the same time by pausing each MCP that is updated by the new machine config file.

.Procedure

1. Pause the affected MCP by running the following command:
```bash
$ oc patch mcp/<mcp_name> --type merge --patch '{"spec":{"paused":true}}'
```

1. After you apply all machine config changes to the cluster, run the following command:
```bash
$ oc patch mcp/<mcp_name> --type merge --patch '{"spec":{"paused":false}}'
```

This allows the nodes in your MCP to reboot into the new configurations.
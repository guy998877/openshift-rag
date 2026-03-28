# Pausing the machine config pools

After you create your custom machine config pools (MCPs), you then pause those MCPs. Pausing an MCP prevents the Machine Config Operator (MCO) from updating the nodes associated with that MCP.

.Procedure

1. Patch the MCP that you want paused by running the following command:
```bash
$ oc patch mcp/<mcp_name> --patch '{"spec":{"paused":true}}' --type=merge
```
For example:
```bash
$  oc patch mcp/workerpool-canary --patch '{"spec":{"paused":true}}' --type=merge
```
.Example output
```bash
machineconfigpool.machineconfiguration.openshift.io/workerpool-canary patched
```
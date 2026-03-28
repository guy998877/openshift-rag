# Pausing worker nodes before the update

You must pause the worker nodes before you proceed with the update.
In the following example, there are 2 `mcp` groups, `mcp-1` and `mcp-2`.
You patch the `spec.paused` field to `true` for each of the `MachineConfigPool` groups.

.Procedure

1. Patch the `mcp` CRs to pause the nodes and drain and remove the pods from those nodes by running the following command:
```bash
$ oc patch mcp/mcp-1 --type merge --patch '{"spec":{"paused":true}}'
```
```bash
$ oc patch mcp/mcp-2 --type merge --patch '{"spec":{"paused":true}}'
```

1. Get the status of the paused `mcp` groups:
```bash
$ oc get mcp -o json | jq -r '["MCP","Paused"], ["---","------"], (.items[] | [(.metadata.name), (.spec.paused)]) | @tsv' | grep -v worker
```
.Example output
```bash
MCP     Paused
---     ------
master  false
mcp-1   true
mcp-2   true
```

> **NOTE:** The default control plane and worker `mcp` groups are not changed during an update.
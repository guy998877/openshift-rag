# Reserving resources for system processes

You can explicitly reserve resources for non-pod processes by allocating node resources through specifying resources available for scheduling.

To provide more reliable scheduling and minimize node resource overcommitment, each node can reserve a portion of its resources for use by the system daemons that are required to run on your node for your cluster to function.

> **NOTE:** It is recommended that you reserve resources for incompressible resources such as memory.

For more details, see Allocating Resources for Nodes in the _Additional resources_ section.
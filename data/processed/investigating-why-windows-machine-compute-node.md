# Investigating why Windows Machine does not become compute node

There are various reasons why a Windows Machine does not become a compute node. The best way to investigate this problem is to collect the Windows Machine Config Operator (WMCO) logs.

.Prerequisites

- You installed the Windows Machine Config Operator (WMCO) using Operator Lifecycle Manager (OLM).
- You have created a Windows compute machine set.

.Procedure

- Run the following command to collect the WMCO logs:
```bash
$ oc logs -f deployment/windows-machine-config-operator -n openshift-windows-machine-config-operator
```
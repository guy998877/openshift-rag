# Adding more compute machines to a cluster in vSphere

You can add more compute machines to a user-provisioned OpenShift Container Platform cluster on VMware vSphere.

After your vSphere template deploys in your OpenShift Container Platform cluster, you can deploy a virtual machine (VM) for a machine in that cluster.

.Prerequisites

- Obtain the base64-encoded Ignition file for your compute machines.
- You have access to the vSphere template that you created for your cluster.

.Procedure

1. Right-click the template's name and click *Clone* -> *Clone to Virtual Machine*.

1. On the *Select a name and folder* tab, specify a name for the VM. You might include the machine type in the name, such as `compute-1`.
> **NOTE:** Ensure that all virtual machine names across a vSphere installation are unique.

1. On the *Select a name and folder* tab, select the name of the folder that you created for the cluster.

1. On the *Select a compute resource* tab, select the name of a host in your data center.

1. On the *Select storage* tab, select storage for your configuration and disk files.

1. On the *Select clone options* tab, select *Customize this virtual machine's hardware*.

1. On the *Customize hardware* tab, click *Advanced Parameters*.
- Add the following configuration parameter names and values by specifying data in the *Attribute* and *Values* fields. Ensure that you select the *Add* button for each parameter that you create.
- `guestinfo.ignition.config.data`: Paste the contents of the base64-encoded compute Ignition config file for this machine type.
- `guestinfo.ignition.config.data.encoding`: Specify `base64`.
- `disk.EnableUUID`: Specify `TRUE`.

1. In the *Virtual Hardware* panel of the *Customize hardware* tab, modify the specified values as required. Ensure that the amount of RAM, CPU, and disk storage meets the minimum requirements for the machine type. If many networks exist, select *Add New Device* > *Network Adapter*, and then enter your network information in the fields provided by the *New Network* menu item.

1. Complete the remaining configuration steps. On clicking the *Finish* button, you have completed the cloning operation.

1. From the *Virtual Machines* tab, right-click on your VM and then select *Power* -> *Power On*.

.Next steps

- Continue to create more compute machines for your cluster.
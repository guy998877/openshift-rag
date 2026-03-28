# Understanding the difference between compute machine sets and the machine config pool

`MachineSet` objects describe OpenShift Container Platform nodes with respect to the cloud or machine provider.

The `MachineConfigPool` object allows `MachineConfigController` components to define and provide the status of machines in the context of upgrades.

The `MachineConfigPool` object allows users to configure how upgrades are rolled out to the OpenShift Container Platform nodes in the machine config pool.

The `NodeSelector` object can be replaced with a reference to the `MachineSet` object.
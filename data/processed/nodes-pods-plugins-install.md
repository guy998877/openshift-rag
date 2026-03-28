# Enabling Device Manager

Enable Device Manager to implement a device plugin to advertise specialized
hardware without any upstream code changes.

Device Manager provides a mechanism for advertising specialized node hardware resources
with the help of plugins known as device plugins.

1. Obtain the label associated with the static `MachineConfigPool` CRD for the type of node you want to configure by entering the following command.
Perform one of the following steps:

.. View the machine config:
```bash
# oc describe machineconfig <name>
```
For example:
```bash
# oc describe machineconfig 00-worker
```
.Example output
```bash
Name:         00-worker
Namespace:
Labels:       machineconfiguration.openshift.io/role=worker <1>
```
<1> Label required for the Device Manager.

.Procedure

1. Create a custom resource (CR) for your configuration change.
.Sample configuration for a Device Manager CR
```yaml
apiVersion: machineconfiguration.openshift.io/v1
kind: KubeletConfig
metadata:
  name: devicemgr <1>
spec:
  machineConfigPoolSelector:
    matchLabels:
       machineconfiguration.openshift.io: devicemgr <2>
  kubeletConfig:
    feature-gates:
      - DevicePlugins=true <3>
```
<1> Assign a name to CR.
<2> Enter the label from the Machine Config Pool.
<3> Set `DevicePlugins` to 'true`.

1. Create the Device Manager:
```bash
$ oc create -f devicemgr.yaml
```
.Example output
```bash
kubeletconfig.machineconfiguration.openshift.io/devicemgr created
```

1. Ensure that Device Manager was actually enabled by confirming that
*_/var/lib/kubelet/device-plugins/kubelet.sock_* is created on the node. This is
the UNIX domain socket on which the Device Manager gRPC server listens for new
plugin registrations. This sock file is created when the Kubelet is started
only if Device Manager is enabled.
# Creating the new control plane node

Begin creating the new control plane node by creating a `BareMetalHost` object and node.

.Procedure

1. Edit the `bmh_affected.yaml` file that you previously saved:
--
.. Remove the following metadata items from the file:
- `creationTimestamp`
- `generation`
- `resourceVersion`
- `uid`

.. Remove the `status` section of the file.
--
The resulting file should resemble the following example:
.Example `bmh_affected.yaml` file
```yaml
apiVersion: metal3.io/v1alpha1
kind: BareMetalHost
metadata:
  labels:
    installer.openshift.io/role: control-plane
  name: openshift-control-plane-2
  namespace: openshift-machine-api
spec:
  automatedCleaningMode: disabled
  bmc:
    address:
    credentialsName:
    disableCertificateVerification: true
  bootMACAddress: ab:cd:ef:ab:cd:ef
  bootMode: UEFI
  externallyProvisioned: true
  online: true
  rootDeviceHints:
    deviceName: /dev/disk/by-path/pci-0000:04:00.0-nvme-1
  userData:
    name: master-user-data-managed
    namespace: openshift-machine-api
```

1. Create the `BareMetalHost` object using the `bmh_affected.yaml` file by running the following command:
```bash
$ oc create -f bmh_affected.yaml
```
The following warning is expected upon creation of the `BareMetalHost` object:
```bash
Warning: metadata.finalizers: "baremetalhost.metal3.io": prefer a domain-qualified finalizer name to avoid accidental conflicts with other finalizer writers
```

1. Extract the control plane ignition secret by running the following command:
```bash
$ oc extract secret/master-user-data-managed \
    -n openshift-machine-api \
    --keys=userData \
    --to=- \
    | sed '/^userData/d' > new_controlplane.ign
```
This command also removes the starting `userData` line of the ignition secret.

1. Create an Nmstate YAML file titled `new_controlplane_nmstate.yaml` for the new node's network configuration, using the following example for reference:
.Example Nmstate YAML file
```yaml
interfaces:
  - name: eno1
    type: ethernet
    state: up
    mac-address: "ab:cd:ef:01:02:03"
    ipv4:
      enabled: true
      address:
        - ip: 192.168.20.11
          prefix-length: 24
      dhcp: false
    ipv6:
      enabled: false
dns-resolver:
  config:
    search:
      - iso.sterling.home
    server:
      - 192.168.20.8
routes:
  config:
  - destination: 0.0.0.0/0
    metric: 100
    next-hop-address: 192.168.20.1
    next-hop-interface: eno1
    table-id: 254
```
> **NOTE:** If you installed your cluster using the Agent-based Installer, you can use the failed node's `networkConfig` section in the `agent-config.yaml` file from the original cluster deployment as a starting point for the new control plane node's Nmstate file. For example, the following command extracts the `networkConfig` section for the first control plane node: [source,terminal] ---- $ cat agent-config-iso.yaml | yq .hosts[0].networkConfig > new_controlplane_nmstate.yaml ----

1. Create the customized Red Hat Enterprise Linux CoreOS (RHCOS) live ISO by running the following command:
```bash
$ coreos-installer iso customize rhcos-live.86_64.iso \
    --dest-ignition new_controlplane.ign \
    --network-nmstate new_controlplane_nmstate.yaml \
    --dest-device /dev/disk/by-path/<device_path> \
    -f
```
Replace `<device_path>` with the path to the target device on which the ISO will be generated.

1. Boot the new control plane node with the customized RHCOS live ISO.

1. Approve the Certificate Signing Requests (CSR) to join the new node to the cluster.
// Assumption is that attribute once outside ifdef works for several level one headings.

.Prerequisites

- You have a domain name server (DNS) that can perform hostname and reverse lookup for the nodes.
- You have an HTTP or HTTPS server running on your provisioning machine that is accessible to the machines you create.

.Procedure

1. Extract the Ignition config file from the cluster by running the following command:
```bash
$ oc extract -n openshift-machine-api secret/worker-user-data-managed --keys=userData --to=- > worker.ign
```

1. Upload the `worker.ign` Ignition config file you exported from your cluster to your HTTP server. Note the URL of this file.

1. You can validate that the Ignition file is available on the URL. The following example gets the Ignition config file for the compute node:
```bash
$ curl -k http://<http_server>/worker.ign
```

1. Download the RHEL live `kernel`, `initramfs`, and `rootfs` files by running the following commands:
```bash
$ curl -LO $(oc -n openshift-machine-config-operator get configmap/coreos-bootimages -o jsonpath='{.data.stream}' \
| jq -r '.architectures.s390x.artifacts.metal.formats.pxe.kernel.location')
```
```bash
$ curl -LO $(oc -n openshift-machine-config-operator get configmap/coreos-bootimages -o jsonpath='{.data.stream}' \
| jq -r '.architectures.s390x.artifacts.metal.formats.pxe.initramfs.location')
```
```bash
$ curl -LO $(oc -n openshift-machine-config-operator get configmap/coreos-bootimages -o jsonpath='{.data.stream}' \
| jq -r '.architectures.s390x.artifacts.metal.formats.pxe.rootfs.location')
```

1. Move the downloaded RHEL live `kernel`, `initramfs`, and `rootfs` files to an HTTP or HTTPS server that is accessible from the RHCOS guest you want to add.

1. Create a parameter file for the guest. The following parameters are specific for the virtual machine:
- Optional: To specify a static IP address, add an `ip=` parameter with the following entries, with each separated by a colon:
... The IP address for the machine.
... An empty string.
... The gateway.
... The netmask.
... The machine host and domain name in the form `hostname.domainname`. If you omit this value, RHCOS obtains the hostname through a reverse DNS lookup.
... The network interface name. If you omit this value, RHCOS applies the IP configuration to all available interfaces.
... The value `none`.
- For `coreos.inst.ignition_url=`, specify the URL to the `worker.ign` file. Only HTTP and HTTPS protocols are supported.
- For `coreos.live.rootfs_url=`, specify the matching rootfs artifact for the `kernel` and `initramfs` you are booting. Only HTTP and HTTPS protocols are supported.

- For installations on DASD-type disks, complete the following tasks:
... For `coreos.inst.install_dev=`, specify `/dev/dasda`.
... Use `rd.dasd=` to specify the DASD where RHCOS is to be installed.
... You can adjust further parameters if required.
The following is an example parameter file, `additional-worker-dasd.parm`:
```bash
cio_ignore=all,!condev rd.neednet=1 \
console=ttysclp0 \
coreos.inst.install_dev=/dev/dasda \
coreos.inst.ignition_url=http://<http_server>/worker.ign \
coreos.live.rootfs_url=http://<http_server>/rhcos-<version>-live-rootfs.<architecture>.img \
ip=<ip>::<gateway>:<netmask>:<hostname>::none nameserver=<dns> \
rd.znet=qeth,0.0.bdf0,0.0.bdf1,0.0.bdf2,layer2=1,portno=0 \
rd.dasd=0.0.3490 \
zfcp.allow_lun_scan=0
```
Write all options in the parameter file as a single line and make sure that you have no newline characters.

- For installations on FCP-type disks, complete the following tasks:
... Use `rd.zfcp=<adapter>,<wwpn>,<lun>` to specify the FCP disk where RHCOS is to be installed. For multipathing, repeat this step for each additional path.
> **NOTE:** When you install with multiple paths, you must enable multipathing directly after the installation, not at a later point in time, as this can cause problems.
... Set the install device as: `coreos.inst.install_dev=/dev/sda`.
> **NOTE:** If additional LUNs are configured with NPIV, FCP requires `zfcp.allow_lun_scan=0`. If you must enable `zfcp.allow_lun_scan=1` because you use a CSI driver, for example, you must configure your NPIV so that each node cannot access the boot partition of another node.
... You can adjust further parameters if required.
> **IMPORTANT:** Additional postinstallation steps are required to fully enable multipathing. For more information, see “Enabling multipathing with kernel arguments on RHCOS" in _Machine configuration_.
// Add xref once it's allowed.
The following is an example parameter file, `additional-worker-fcp.parm` for a worker node with multipathing:
```bash
cio_ignore=all,!condev rd.neednet=1 \
console=ttysclp0 \
coreos.inst.install_dev=/dev/sda \
coreos.live.rootfs_url=http://<http_server>/rhcos-<version>-live-rootfs.<architecture>.img \
coreos.inst.ignition_url=http://<http_server>/worker.ign \
ip=<ip>::<gateway>:<netmask>:<hostname>::none nameserver=<dns> \
rd.znet=qeth,0.0.bdf0,0.0.bdf1,0.0.bdf2,layer2=1,portno=0 \
zfcp.allow_lun_scan=0 \
rd.zfcp=0.0.1987,0x50050763070bc5e3,0x4008400B00000000 \
rd.zfcp=0.0.19C7,0x50050763070bc5e3,0x4008400B00000000 \
rd.zfcp=0.0.1987,0x50050763071bc5e3,0x4008400B00000000 \
rd.zfcp=0.0.19C7,0x50050763071bc5e3,0x4008400B00000000
```
Write all options in the parameter file as a single line and make sure that you have no newline characters.
# Creating RHCOS machines using `virt-install`

You can create more Red Hat Enterprise Linux CoreOS (RHCOS) compute machines for your cluster by using `virt-install`.

.Prerequisites

- You have at least one LPAR running on RHEL 8.7 or later with KVM, referred to as RHEL KVM host in this procedure.
- The KVM/QEMU hypervisor is installed on the RHEL KVM host.
- You have a domain name server (DNS) that can perform hostname and reverse lookup for the nodes.
- An HTTP or HTTPS server is set up.

.Procedure

1. Extract the Ignition config file from the cluster by running the following command:
```bash
$ oc extract -n openshift-machine-api secret/worker-user-data-managed --keys=userData --to=- > worker.ign
```

1. Upload the `worker.ign` Ignition config file you exported from your cluster to your HTTP server. Note the URL of this file.

1. You can validate that the Ignition file is available on the URL. The following example gets the Ignition config file for the compute node:
```bash
$ curl -k http://<HTTP_server>/worker.ign
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

1. Move the downloaded RHEL live `kernel`, `initramfs`, and `rootfs` files to an HTTP or HTTPS server before you launch `virt-install`.

1. Create the new KVM guest nodes using the RHEL `kernel`, `initramfs`, and Ignition files; the new disk image; and adjusted parm line arguments.
--
```bash
$ virt-install \
   --connect qemu:///system \
   --name <vm_name> \
   --autostart \
   --os-variant rhel9.4 \ <1>
   --cpu host \
   --vcpus <vcpus> \
   --memory <memory_mb> \
   --disk <vm_name>.qcow2,size=<image_size> \
   --network network=<virt_network_parm> \
   --location <media_location>,kernel=<rhcos_kernel>,initrd=<rhcos_initrd> \ <2>
   --extra-args "rd.neednet=1" \
   --extra-args "coreos.inst.install_dev=/dev/vda" \
   --extra-args "coreos.inst.ignition_url=http://<http_server>/worker.ign " \ <3>
   --extra-args "coreos.live.rootfs_url=http://<http_server>/rhcos-<version>-live-rootfs.<architecture>.img" \ <4>
   --extra-args "ip=<ip>::<gateway>:<netmask>:<hostname>::none" \ <5>
   --extra-args "nameserver=<dns>" \
   --extra-args "console=ttysclp0" \
   --noautoconsole \
   --wait
```
<1> For `os-variant`, specify the RHEL version for the RHCOS compute machine. `rhel9.4` is the recommended version. To query the supported RHEL version of your operating system, run the following command:
```bash
$ osinfo-query os -f short-id
```
> **NOTE:** The `os-variant` is case sensitive.
<2> For `--location`, specify the location of the kernel/initrd on the HTTP or HTTPS server.
<3> Specify the location of the `worker.ign` config file. Only HTTP and HTTPS protocols are supported.
<4> Specify the location of the `rootfs` artifact for the `kernel` and `initramfs` you are booting. Only HTTP and HTTPS protocols are supported
<5> Optional: For `hostname`, specify the fully qualified hostname of the client machine.
--
> **NOTE:** If you are using HAProxy as a load balancer, update your HAProxy rules for `ingress-router-443` and `ingress-router-80` in the `/etc/haproxy/haproxy.cfg` configuration file.

1. Continue to create more compute machines for your cluster.
# Adding worker nodes to single-node OpenShift clusters manually

You can add a worker node to a single-node OpenShift cluster manually by booting the worker node from Red Hat Enterprise Linux CoreOS (RHCOS) ISO and by using the cluster `worker.ign` file to join the new worker node to the cluster.

.Prerequisites

- Install a single-node OpenShift cluster on bare metal.

- Install the OpenShift CLI (`oc`).

- Log in as a user with `cluster-admin` privileges.

- Ensure that all the required DNS records exist for the cluster that you are adding the worker node to.

.Procedure

1. Set the OpenShift Container Platform version:
```bash
$ OCP_VERSION=<ocp_version>
```
Replace `<ocp_version>` with the current version, for example, `latest-4.21`

1. Set the host architecture:
```bash
$ ARCH=<architecture>
```
Replace `<architecture>` with the target host architecture, for example, `aarch64` or `x86_64`.

1. Get the `worker.ign` data from the running single-node cluster by running the following command:
```bash
$ oc extract -n openshift-machine-api secret/worker-user-data-managed --keys=userData --to=- > worker.ign
```

1. Host the `worker.ign` file on a web server accessible from your network.

1. Download the OpenShift Container Platform installer and make it available for use by running the following commands:
```bash
$ curl -k https://mirror.openshift.com/pub/openshift-v4/clients/ocp/$OCP_VERSION/openshift-install-linux.tar.gz > openshift-install-linux.tar.gz
```
```bash
$ tar zxvf openshift-install-linux.tar.gz
```
```bash
$ chmod +x openshift-install
```

1. Retrieve the RHCOS ISO URL:
```bash
$ ISO_URL=$(./openshift-install coreos print-stream-json | grep location | grep $ARCH | grep iso | cut -d\" -f4)
```

1. Download the RHCOS ISO:
```bash
$ curl -L $ISO_URL -o rhcos-live.iso
```

1. Use the RHCOS ISO and the hosted `worker.ign` file to install the worker node:

.. Boot the target host with the RHCOS ISO and your preferred method of installation.

.. When the target host has booted from the RHCOS ISO, open a console on the target host.

.. If your local network does not have DHCP enabled, you need to create an ignition file with the new hostname and configure the worker node static IP address before running the RHCOS installation. Perform the following steps:

... Configure the worker host network connection with a static IP. Run the following command on the target host console:
```bash
$ nmcli con mod <network_interface> ipv4.method manual /
ipv4.addresses <static_ip> ipv4.gateway <network_gateway> ipv4.dns <dns_server> /
802-3-ethernet.mtu 9000
```
where:
--
<static_ip>:: Specifies the host static IP address and CIDR, for example, `10.1.101.50/24`.
<network_gateway>:: Specifies the network gateway, for example, `10.1.101.1`.
--

... Activate the modified network interface:
```bash
$ nmcli con up <network_interface>
```

... Create a new ignition file `new-worker.ign` that includes a reference to the original `worker.ign` and an additional instruction that the `coreos-installer` program uses to populate the `/etc/hostname` file on the new worker host. For example:
```json
{
  "ignition":{
    "version":"3.2.0",
    "config":{
      "merge":[
        {
          "source":"<hosted_worker_ign_file>"
        }
      ]
    }
  },
  "storage":{
    "files":[
      {
        "path":"/etc/hostname",
        "contents":{
          "source":"data:,<new_fqdn>"
        },
        "mode":420,
        "overwrite":true,
        "path":"/etc/hostname"
      }
    ]
  }
}
```
where:
`<hosted_worker_ign_file>`:: Specifies the locally accessible URL for the original `worker.ign` file. For example, `http://webserver.example.com/worker.ign`.
`<new_fqdn>`:: Specifies the new FQDN that you set for the worker node. For example, `new-worker.example.com`.

... Host the `new-worker.ign` file on a web server accessible from your network.

... Run the following `coreos-installer` command, passing in the `ignition-url` and hard disk details:
```bash
$ sudo coreos-installer install --copy-network /
--ignition-url=<new_worker_ign_file> <hard_disk> --insecure-ignition
```
where:
--
<new_worker_ign_file>:: Specifies the locally accessible URL for the hosted `new-worker.ign` file, for example, `http://webserver.example.com/new-worker.ign`.
<hard_disk>:: Specifies the hard disk where you install RHCOS, for example, `/dev/sda`.
--

.. For networks that have DHCP enabled, you do not need to set a static IP. Run the following `coreos-installer` command from the target host console to install the system:
```bash
$ coreos-installer install --ignition-url=<hosted_worker_ign_file> <hard_disk>
```

.. To manually enable DHCP, apply the following `NMStateConfig` CR to the single-node OpenShift cluster:
```yaml
apiVersion: agent-install.openshift.io/v1
kind: NMStateConfig
metadata:
  name: nmstateconfig-dhcp
  namespace: example-sno
  labels:
    nmstate_config_cluster_name: <nmstate_config_cluster_label>
spec:
  config:
    interfaces:
      - name: eth0
        type: ethernet
        state: up
        ipv4:
          enabled: true
          dhcp: true
        ipv6:
          enabled: false
  interfaces:
    - name: "eth0"
      macAddress: "AA:BB:CC:DD:EE:11"
```
> **IMPORTANT:** The `NMStateConfig` CR is required for successful deployment of worker nodes with static IP addresses and for adding a worker node with a dynamic IP address if the single-node OpenShift was deployed with a static IP address. The cluster network DHCP does not automatically set these network settings for the new worker node.

1. As the installation proceeds, the installation generates pending certificate signing requests (CSRs) for the worker node. When prompted, approve the pending CSRs to complete the installation.

1. When the installation is complete, reboot the host. The host joins the cluster as a new worker node.

.Verification

- Check that the new worker node was successfully added to the cluster with a status of `Ready`:
```bash
$ oc get nodes
```
.Example output
```bash
NAME                           STATUS   ROLES           AGE   VERSION
control-plane-1.example.com    Ready    master,worker   56m   v1.34.2
compute-1.example.com          Ready    worker          11m   v1.34.2
```
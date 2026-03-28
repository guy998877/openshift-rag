# Configuring RHOSP clusters that have machines with root volume availability zones after an upgrade

For some clusters that run on Red Hat OpenStack Platform (RHOSP) that you upgrade, you must manually update machine resources before you can use control plane machine sets if the following configurations are true:

- The upgraded cluster was created with OpenShift Container Platform 4.13 or earlier.

- The cluster infrastructure is installer-provisioned.

- Machines were distributed across multiple availability zones.

- Machines were configured to use root volumes for which block storage availability zones were not defined.

To understand why this procedure is necessary, see [Solution #7024383](https://access.redhat.com/solutions/7013893).

.Procedure

1. For all control plane machines, edit the provider spec for all control plane machines that match the environment. For example, to edit the machine `master-0`, enter the following command:
```bash
$ oc edit machine/<cluster_id>-master-0 -n openshift-machine-api
```
where:
`<cluster_id>`:: Specifies the ID of the upgraded cluster.

1. In the provider spec, set the value of the property `rootVolume.availabilityZone` to the volume of the availability zone you want to use.
.An example RHOSP provider spec
```yaml
providerSpec:
  value:
    apiVersion: machine.openshift.io/v1alpha1
    availabilityZone: az0
      cloudName: openstack
    cloudsSecret:
      name: openstack-cloud-credentials
      namespace: openshift-machine-api
    flavor: m1.xlarge
    image: rhcos-4.14
    kind: OpenstackProviderSpec
    metadata:
      creationTimestamp: null
    networks:
    - filter: {}
      subnets:
      - filter:
          name: refarch-lv7q9-nodes
          tags: openshiftClusterID=refarch-lv7q9
    rootVolume:
        availabilityZone: nova <1>
        diskSize: 30
        sourceUUID: rhcos-4.12
        volumeType: fast-0
    securityGroups:
    - filter: {}
      name: refarch-lv7q9-master
    serverGroupName: refarch-lv7q9-master
    serverMetadata:
      Name: refarch-lv7q9-master
      openshiftClusterID: refarch-lv7q9
    tags:
    - openshiftClusterID=refarch-lv7q9
    trunk: true
    userDataSecret:
      name: master-user-data
```
<1> Set the zone name as this value.
> **NOTE:** If you edited or recreated machine resources after your initial cluster deployment, you might have to adapt these steps for your configuration. In your RHOSP cluster, find the availability zone of the root volumes for your machines and use that as the value.

1. Run the following command to retrieve information about the control plane machine set resource:
```bash
$ oc describe controlplanemachineset.machine.openshift.io/cluster --namespace openshift-machine-api
```

1. Run the following command to edit the resource:
```bash
$ oc edit controlplanemachineset.machine.openshift.io/cluster --namespace openshift-machine-api
```

1. For that resource, set the value of the `spec.state` property to `Active` to activate control plane machine sets for your cluster.

Your control plane is ready to be managed by the Cluster Control Plane Machine Set Operator.
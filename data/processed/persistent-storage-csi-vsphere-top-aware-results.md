# Results

Creating persistent volume claims (PVCs) and PVs from the topology aware storage class are truly zonal, and should use the datastore in their respective zone depending on how pods are scheduled:

```bash
$ oc get pv <pv_name> -o yaml
```

.Example output

```bash
...
nodeAffinity:
  required:
    nodeSelectorTerms:
    - matchExpressions:
      - key: topology.csi.vmware.com/openshift-zone <1>
        operator: In
        values:
        - <openshift_zone>
      - key: topology.csi.vmware.com/openshift-region <1>
        operator: In
        values:
        - <openshift_region>
...
peristentVolumeclaimPolicy: Delete
storageClassName: <zoned_storage_class_name> <2>
volumeMode: Filesystem
...
```
<1> PV has zoned keys.
<2> PV is using the zoned storage class.
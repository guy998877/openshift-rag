# Example using the CSI driver

The following example installs a default MySQL template without any
changes to the template.

.Prerequisites

- The CSI driver has been deployed.
- A storage class has been created for dynamic provisioning.

.Procedure

- Create the MySQL template:
```bash
# oc new-app mysql-persistent
```
.Example output
```bash
--> Deploying template "openshift/mysql-persistent" to project default
...
```
```bash
# oc get pvc
```
.Example output
```bash
NAME              STATUS    VOLUME                                   CAPACITY
ACCESS MODES   STORAGECLASS   AGE
mysql             Bound     kubernetes-dynamic-pv-3271ffcb4e1811e8   1Gi
RWO            cinder         3s
```
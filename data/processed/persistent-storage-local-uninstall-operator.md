# Uninstalling the Local Storage Operator

To uninstall the Local Storage Operator, you must remove the Operator and all created resources in the `openshift-local-storage` project.

> **WARNING:** Uninstalling the Local Storage Operator while local storage PVs are still in use is not recommended. While the PVs will remain after the Operator's removal, there might be indeterminate behavior if the Operator is uninstalled and reinstalled without removing the PVs and local storage resources.

.Prerequisites

- Access to the OpenShift Container Platform web console.

.Procedure

1. Delete any local volume resources installed in the project, such as `localvolume`, `localvolumeset`, and `localvolumediscovery` by running the following commands:
```bash
$ oc delete localvolume --all --all-namespaces
```
```bash
$ oc delete localvolumeset --all --all-namespaces
```
```bash
$ oc delete localvolumediscovery --all --all-namespaces
```

1. Uninstall the Local Storage Operator from the web console.

.. Log in to the OpenShift Container Platform web console.

.. Navigate to *Ecosystem* -> *Installed Operators*.

.. Type *Local Storage* into the filter box to locate the Local Storage Operator.

.. Click the Options menu image:kebab.png[title="Options menu"] at the end of the Local Storage Operator.

.. Click *Uninstall Operator*.

.. Click *Remove* in the window that appears.

1. The PVs created by the Local Storage Operator will remain in the cluster until deleted. After these volumes are no longer in use, delete them by running the following command:
```bash
$ oc delete pv <pv-name>
```

1. Delete the `openshift-local-storage` project by running the following command:
```bash
$ oc delete project openshift-local-storage
```
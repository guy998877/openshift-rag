# Software catalog architecture

The software catalog UI component is driven by the Marketplace Operator by default on OpenShift Container Platform in the `openshift-marketplace` namespace.

## OperatorHub custom resource

The Marketplace Operator manages an `OperatorHub` custom resource (CR) named `cluster` that manages the default `CatalogSource` objects provided with the software catalog.
You can modify this resource to enable or disable the default catalogs, which is useful when configuring OpenShift Container Platform in restricted network environments.

.Example `OperatorHub` custom resource
```yaml
apiVersion: config.openshift.io/v1
kind: OperatorHub
metadata:
  name: cluster
spec:
  disableAllDefaultSources: true <1>
  sources: [ <2>
    {
      name: "community-operators",
      disabled: false
    }
  ]
```
<1> `disableAllDefaultSources` is an override that controls availability of all default catalogs that are configured by default during an OpenShift Container Platform installation.
<2> Disable default catalogs individually by changing the `disabled` parameter value per source.
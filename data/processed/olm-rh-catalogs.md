:tag: v4.21
:global_ns: openshift-marketplace

# About Red Hat-provided Operator catalogs

The Red Hat-provided catalog sources are installed by default in the `openshift-operators` namespace, which makes the catalogs available cluster-wide in all namespaces.

The following Operator catalogs are distributed by Red Hat:

[cols="20%,55%,25%",options="header"]
|===
|Catalog
|Index image
|Description

|`redhat-operators`
|`registry.redhat.io/redhat/redhat-operator-index:{tag}`
|Red Hat products packaged and shipped by Red Hat. Supported by Red Hat.

|`certified-operators`
|`registry.redhat.io/redhat/certified-operator-index:{tag}`
|Products from leading independent software vendors (ISVs). Red Hat partners with ISVs to package and ship. Supported by the ISV.

// |`redhat-marketplace`
// |`registry.redhat.io/redhat/redhat-marketplace-index:{tag}`
// |Certified software that can be purchased from [Red Hat Marketplace](https://marketplace.redhat.com/).

|`community-operators`
|`registry.redhat.io/redhat/community-operator-index:{tag}`
|Software maintained by relevant representatives in the [redhat-openshift-ecosystem/community-operators-prod/operators](https://github.com/redhat-openshift-ecosystem/community-operators-prod/tree/main/operators) GitHub repository. No official support.
|===

During a cluster upgrade, the index image tag for the default Red Hat-provided catalog sources are updated automatically by the Cluster Version Operator (CVO) so that Operator Lifecycle Manager (OLM) pulls the updated version of the catalog. For example during an upgrade from OpenShift Container Platform 4.8 to 4.9, the `spec.image` field in the `CatalogSource` object for the `redhat-operators` catalog is updated from:

```bash
registry.redhat.io/redhat/redhat-operator-index:v4.8
```

to:

```bash
registry.redhat.io/redhat/redhat-operator-index:v4.9
```

:!tag:
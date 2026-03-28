# Configuring catalogs to run with elevated permissions

If you do not want to update your SQLite database catalog image or migrate your catalog to the file-based catalog format, you can perform the following actions to ensure your catalog source runs when the default pod security enforcement changes to restricted:

- Manually set the catalog security mode to legacy in your catalog source definition. This action ensures your catalog runs with legacy permissions even if the default catalog security mode changes to restricted.
- Label the catalog source namespace for baseline or privileged pod security enforcement.

> **NOTE:** The SQLite database catalog format is deprecated, but still supported by Red Hat. In a future release, the SQLite database format will not be supported, and catalogs will need to migrate to the file-based catalog format. File-based catalogs are compatible with restricted pod security enforcement.

.Prerequisites

- You have a SQLite database catalog source.
- You have access to the cluster as a user with the `cluster-admin` role.
- You have a target namespace that supports running pods with the elevated pod security admission standard of `baseline` or `privileged`.

.Procedure

1. Edit the `CatalogSource` definition by setting the `spec.grpcPodConfig.securityContextConfig` label to `legacy`, as shown in the following example:
.Example `CatalogSource` definition
```yaml
apiVersion: operators.coreos.com/v1alpha1
kind: CatalogSource
metadata:
  name: my-catsrc
  namespace: my-ns
spec:
  sourceType: grpc
  grpcPodConfig:
    securityContextConfig: legacy
  image: my-image:latest
```
> **TIP:** In OpenShift Container Platform 4.21, the `spec.grpcPodConfig.securityContextConfig` field is set to `legacy` by default. In a future release of OpenShift Container Platform, it is planned that the default setting will change to `restricted`. If your catalog cannot run under restricted enforcement, it is recommended that you manually set this field to `legacy`.

1. Edit your `<namespace>.yaml` file to add elevated pod security admission standards to your catalog source namespace, as shown in the following example:
.Example `<namespace>.yaml` file
```yaml
apiVersion: v1
kind: Namespace
metadata:
...
  labels:
    security.openshift.io/scc.podSecurityLabelSync: "false" <1>
    openshift.io/cluster-monitoring: "true"
    pod-security.kubernetes.io/enforce: baseline <2>
  name: "<namespace_name>"
```
<1> Turn off pod security label synchronization by adding the `security.openshift.io/scc.podSecurityLabelSync=false` label to the namespace.
<2> Apply the pod security admission `pod-security.kubernetes.io/enforce` label. Set the label to `baseline` or `privileged`. Use the `baseline` pod security profile unless other workloads in the namespace require a `privileged` profile.
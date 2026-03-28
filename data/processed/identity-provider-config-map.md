# Creating a config map

Identity providers use OpenShift Container Platform `ConfigMap` objects in the `openshift-config`
namespace to contain the certificate authority bundle. These are primarily
used to contain certificate bundles needed by the identity provider.

.Procedure

- Define an OpenShift Container Platform `ConfigMap` object containing the
certificate authority by using the following command. The certificate
authority must be stored in the `ca.crt` key of the `ConfigMap` object.
```bash
$ oc create configmap ca-config-map --from-file=ca.crt=/path/to/ca -n openshift-config
```
> **TIP:** You can alternatively apply the following YAML to create the config map: [source,yaml] ---- apiVersion: v1 kind: ConfigMap metadata: name: ca-config-map namespace: openshift-config data: ca.crt: | <CA_certificate_PEM> ----

// Undefining attributes
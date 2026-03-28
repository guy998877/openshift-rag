# Creating the secret

Identity providers use OpenShift Container Platform `Secret` objects in the `openshift-config` namespace to contain the client secret, client certificates, and keys.

.Procedure

- Create a `Secret` object containing a string by using the following command:
```bash
$ oc create secret generic <secret_name> --from-literal=clientSecret=<secret> -n openshift-config
```
> **TIP:** You can alternatively apply the following YAML to create the secret: [source,yaml] ---- apiVersion: v1 kind: Secret metadata: name: <secret_name> namespace: openshift-config type: Opaque data: clientSecret: <base64_encoded_client_secret> ----

- You can define a `Secret` object containing the contents of a file by using the following command:
```bash
$ oc create secret generic <secret_name> --from-file=<path_to_file> -n openshift-config
```
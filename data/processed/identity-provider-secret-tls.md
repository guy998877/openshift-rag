# Creating the secret

Identity providers use OpenShift Container Platform `Secret` objects in the `openshift-config` namespace to contain the client secret, client certificates, and keys.

.Procedure

- Create a `Secret` object that contains the key and certificate by using the following command:
```bash
$ oc create secret tls <secret_name> --key=key.pem --cert=cert.pem -n openshift-config
```
> **TIP:** You can alternatively apply the following YAML to create the secret: [source,yaml] ---- apiVersion: v1 kind: Secret metadata: name: <secret_name> namespace: openshift-config type: kubernetes.io/tls data: tls.crt: <base64_encoded_cert> tls.key: <base64_encoded_key> ----
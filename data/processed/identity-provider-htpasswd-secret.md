# Creating the htpasswd secret

To use the htpasswd identity provider, you must define a secret that
contains the htpasswd user file.

.Prerequisites

- Create an htpasswd file.

.Procedure

- Create a `Secret` object that contains the htpasswd users file:
```bash
$ oc create secret generic htpass-secret --from-file=htpasswd=<path_to_users.htpasswd> -n openshift-config <1>
```
<1> The secret key containing the users file for the `--from-file` argument must be named `htpasswd`, as shown in the above command.
> **TIP:** You can alternatively apply the following YAML to create the secret: [source,yaml] ---- apiVersion: v1 kind: Secret metadata: name: htpass-secret namespace: openshift-config type: Opaque data: htpasswd: <base64_encoded_htpasswd_file_contents> ----
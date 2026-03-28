# Creating an SSH authentication secret

As an administrator, you can create an SSH authentication secret, which allows you to store data used for SSH authentication. When using this secret type, the `data` parameter of the `Secret` object must contain the SSH credential to use.

.Procedure

1. Create a `Secret` object in a YAML file on a control plane node:
.Example `secret` object
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: secret-ssh-auth
type: kubernetes.io/ssh-auth <1>
data:
  ssh-privatekey: | <2>
          MIIEpQIBAAKCAQEAulqb/Y ...
```
<1> Specifies an SSH authentication secret.
<2> Specifies the SSH key/value pair as the SSH credentials to use.

1. Use the following command to create the `Secret` object:
```bash
$ oc create -f <filename>.yaml
```

1. To use the secret in a pod:

.. Update the pod's service account to reference the secret, as shown in the "Understanding how to create secrets" section.

.. Create the pod, which consumes the secret as an environment variable or as a file (using a `secret` volume), as shown in the "Understanding how to create secrets" section.
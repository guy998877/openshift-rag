# Creating an opaque secret

As an administrator, you can create an opaque secret, which allows you to store unstructured `key:value` pairs that can contain arbitrary values.

.Procedure

1. Create a `Secret` object in a YAML file.
For example:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mysecret
type: Opaque <1>
data:
  username: <username>
  password: <password>
```
<1> Specifies an opaque secret.

1. Use the following command to create a `Secret` object:
```bash
$ oc create -f <filename>.yaml
```

1. To use the secret in a pod:

.. Update the pod's service account to reference the secret, as shown in the "Understanding how to create secrets" section.

.. Create the pod, which consumes the secret as an environment variable or as a file (using a `secret` volume), as shown in the "Understanding how to create secrets" section.
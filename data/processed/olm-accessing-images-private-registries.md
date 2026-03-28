# Accessing images for Operators from private registries

You can access images from Operator from private registries by creating a secret for your registry credentials and adding the secret for use with relevant catalogs.

.Prerequisites

- You have at least one of the following hosted in a private registry:
- An index image or catalog image.
- An Operator bundle image.
- An Operator or Operand image.
- You have access to the cluster as a user with the `cluster-admin` role.

.Procedure

1. Create a secret for each required private registry.

.. Log in to the private registry to create or update your registry credentials file:
```bash
$ podman login <registry>:<port>
```
> **NOTE:** The file path of your registry credentials can be different depending on the container tool used to log in to the registry. For the `podman` CLI, the default location is `${XDG_RUNTIME_DIR}/containers/auth.json`. For the `docker` CLI, the default location is `/root/.docker/config.json`.

.. It is recommended to include credentials for only one registry per secret, and manage credentials for multiple registries in separate secrets. Multiple secrets can be included in a `CatalogSource` object in later steps, and OpenShift Container Platform will merge the secrets into a single virtual credentials file for use during an image pull.
A registry credentials file can, by default, store details for more than one registry or for multiple repositories in one registry. Verify the current contents of your file. For example:
.File storing credentials for multiple registries
```json
{
    "auths": {
        "registry.redhat.io": {
            "auth": "FrNHNydQXdzclNqdg=="
        },
        "quay.io": {
            "auth": "fegdsRib21iMQ=="
        },
        "https://quay.io/my-namespace/my-user/my-image": {
            "auth": "eWfjwsDdfsa221=="
        },
        "https://quay.io/my-namespace/my-user": {
            "auth": "feFweDdscw34rR=="
        },
        "https://quay.io/my-namespace": {
            "auth": "frwEews4fescyq=="
        }
    }
}
```
Because this file is used to create secrets in later steps, ensure that you are storing details for only one registry per file. This can be accomplished by using either of the following methods:
--
- Use the `podman logout <registry>` command to remove credentials for additional registries until only the one registry you want remains.
- Edit your registry credentials file and separate the registry details to be stored in multiple files. For example:
.File storing credentials for one registry
```json
{
        "auths": {
                "registry.redhat.io": {
                        "auth": "FrNHNydQXdzclNqdg=="
                }
        }
}
```
.File storing credentials for another registry
```json
{
        "auths": {
                "quay.io": {
                        "auth": "Xd2lhdsbnRib21iMQ=="
                }
        }
}
```
--

.. Create a secret in the `openshift-marketplace` namespace that contains the authentication credentials for a private registry:
```bash
$ oc create secret generic <secret_name> \
    -n openshift-marketplace \
    --from-file=.dockerconfigjson=<path/to/registry/credentials> \
    --type=kubernetes.io/dockerconfigjson
```
Repeat this step to create additional secrets for any other required private registries, updating the `--from-file` flag to specify another registry credentials file path.

1. Create or update an existing `CatalogSource` object to reference one or more secrets:
--
```yaml
apiVersion: operators.coreos.com/v1alpha1
kind: CatalogSource
metadata:
  name: my-operator-catalog
  namespace: openshift-marketplace
spec:
  sourceType: grpc
  secrets: <1>
  - "<secret_name_1>"
  - "<secret_name_2>"
  grpcPodConfig:
    securityContextConfig: <security_mode> <2>
  image: <registry>:<port>/<namespace>/<image>:<tag>
  displayName: My Operator Catalog
  publisher: <publisher_name>
  updateStrategy:
    registryPoll:
      interval: 30m
```
<1> Add a `spec.secrets` section and specify any required secrets.
<2> Specify the value of `legacy` or `restricted`. If the field is not set, the default value is `legacy`. In a future OpenShift Container Platform release, it is planned that the default value will be `restricted`.
> **NOTE:** If your catalog cannot run with `restricted` permissions, it is recommended that you manually set this field to `legacy`.
--

1. If any Operator or Operand images that are referenced by a subscribed Operator require access to a private registry, you can either provide access to all namespaces in the cluster, or individual target tenant namespaces.

- To provide access to all namespaces in the cluster, add authentication details to the global cluster pull secret in the `openshift-config` namespace.
> **WARNING:** Cluster resources must adjust to the new global pull secret, which can temporarily limit the usability of the cluster.

.. Extract the `.dockerconfigjson` file from the global pull secret:
```bash
$ oc extract secret/pull-secret -n openshift-config --confirm
```

.. Update the `.dockerconfigjson` file with your authentication credentials for the required private registry or registries and save it as a new file:
```bash
$ cat .dockerconfigjson | \
    jq --compact-output '.auths["<registry>:<port>/<namespace>/"] |= . + {"auth":"<token>"}' \//<1>
    > new_dockerconfigjson
```
<1> Replace `<registry>:<port>/<namespace>` with the private registry details and `<token>` with your authentication credentials.

.. Update the global pull secret with the new file:
```bash
$ oc set data secret/pull-secret -n openshift-config \
    --from-file=.dockerconfigjson=new_dockerconfigjson
```

- To update an individual namespace, add a pull secret to the service account for the Operator that requires access in the target tenant namespace.

.. Recreate the secret that you created for the `openshift-marketplace` in the tenant namespace:
```bash
$ oc create secret generic <secret_name> \
    -n <tenant_namespace> \
    --from-file=.dockerconfigjson=<path/to/registry/credentials> \
    --type=kubernetes.io/dockerconfigjson
```

.. Verify the name of the service account for the Operator by searching the tenant namespace:
--
```bash
$ oc get sa -n <tenant_namespace> <1>
```
<1> If the Operator was installed in an individual namespace, search that namespace. If the Operator was installed for all namespaces, search the `openshift-operators` namespace.
--
--
.Example output
```bash
NAME            SECRETS   AGE
builder         2         6m1s
default         2         6m1s
deployer        2         6m1s
etcd-operator   2         5m18s <1>
```
<1> Service account for an installed etcd Operator.
--

.. Link the secret to the service account for the Operator:
```bash
$ oc secrets link <operator_sa> \
    -n <tenant_namespace> \
     <secret_name> \
    --for=pull
```
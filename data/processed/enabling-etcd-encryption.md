# Enabling etcd encryption

You can enable etcd encryption to encrypt sensitive resources in your cluster.

> **WARNING:** Do not back up etcd resources until the initial encryption process is completed. If the encryption process is not completed, the backup might be only partially encrypted. After you enable etcd encryption, several changes can occur: * The etcd encryption might affect the memory consumption of a few resources. * You might notice a transient affect on backup performance because the leader must serve the backup. * A disk I/O can affect the node that receives the backup state.

You can encrypt the etcd database in either AES-GCM or AES-CBC encryption.

> **NOTE:** To migrate your etcd database from one encryption type to the other, you can modify the API server's `spec.encryption.type` field. Migration of the etcd data to the new encryption type occurs automatically.

.Prerequisites

- Access to the cluster as a user with the `cluster-admin` role.

.Procedure

1. Modify the `APIServer` object:
```bash
$ oc edit apiserver
```

1. Set the `spec.encryption.type` field to `aesgcm` or `aescbc`:
```yaml
spec:
  encryption:
    type: aesgcm <1>
```
<1> Set to `aesgcm` for AES-GCM encryption or `aescbc` for AES-CBC encryption.

1. Save the file to apply the changes.
The encryption process starts. It can take 20 minutes or longer for this process to complete, depending on the size of the etcd database.

1. Verify that etcd encryption was successful.

.. Review the `Encrypted` status condition for the OpenShift API server to verify that its resources were successfully encrypted:
```bash
$ oc get openshiftapiserver -o=jsonpath='{range .items[0].status.conditions[?(@.type=="Encrypted")]}{.reason}{"\n"}{.message}{"\n"}'
```
The output shows `EncryptionCompleted` upon successful encryption:
```bash
EncryptionCompleted
All resources encrypted: routes.route.openshift.io
```
If the output shows `EncryptionInProgress`, encryption is still in progress. Wait a few minutes and try again.

.. Review the `Encrypted` status condition for the Kubernetes API server to verify that its resources were successfully encrypted:
```bash
$ oc get kubeapiserver -o=jsonpath='{range .items[0].status.conditions[?(@.type=="Encrypted")]}{.reason}{"\n"}{.message}{"\n"}'
```
The output shows `EncryptionCompleted` upon successful encryption:
```bash
EncryptionCompleted
All resources encrypted: secrets, configmaps
```
If the output shows `EncryptionInProgress`, encryption is still in progress. Wait a few minutes and try again.

.. Review the `Encrypted` status condition for the OpenShift OAuth API server to verify that its resources were successfully encrypted:
```bash
$ oc get authentication.operator.openshift.io -o=jsonpath='{range .items[0].status.conditions[?(@.type=="Encrypted")]}{.reason}{"\n"}{.message}{"\n"}'
```
The output shows `EncryptionCompleted` upon successful encryption:
```bash
EncryptionCompleted
All resources encrypted: oauthaccesstokens.oauth.openshift.io, oauthauthorizetokens.oauth.openshift.io
```
If the output shows `EncryptionInProgress`, encryption is still in progress. Wait a few minutes and try again.
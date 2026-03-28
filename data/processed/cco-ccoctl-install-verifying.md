# Verifying that a cluster uses short-term credentials

You can verify that a cluster uses short-term security credentials for individual components by checking the Cloud Credential Operator (CCO) configuration and other values in the cluster.

.Prerequisites

- You deployed an OpenShift Container Platform cluster using the Cloud Credential Operator utility (`ccoctl`) to implement short-term credentials.

- You installed the pass:quotes[OpenShift CLI (`oc`)].

- You are logged in as a user with `cluster-admin` privileges.

.Procedure

- Verify that the CCO is configured to operate in manual mode by running the following command:
```bash
$ oc get cloudcredentials cluster \
  -o=jsonpath={.spec.credentialsMode}
```
The following output confirms that the CCO is operating in manual mode:
.Example output
```text
Manual
```

- Verify that the cluster does not have `root` credentials by running the following command:
```bash
$ oc get secrets \
  -n kube-system <secret_name>
```
where `<secret_name>` is the name of the root secret for your cloud provider.
[cols=2,options=header]
|===
|Platform
|Secret name

|Amazon Web Services (AWS)
|`aws-creds`

|Microsoft Azure
|`azure-credentials`

|Google Cloud
|`gcp-credentials`

|===
An error confirms that the root secret is not present on the cluster.
.Example output for an AWS cluster
```text
Error from server (NotFound): secrets "aws-creds" not found
```

- Verify that the components are using short-term security credentials for individual components by running the following command:
```bash
$ oc get authentication cluster \
  -o jsonpath \
  --template='{ .spec.serviceAccountIssuer }'
```
This command displays the value of the `.spec.serviceAccountIssuer` parameter in the cluster `Authentication` object.
An output of a URL that is associated with your cloud provider indicates that the cluster is using manual mode with short-term credentials that are created and managed from outside of the cluster.

- Azure clusters: Verify that the components are assuming the Azure client ID that is specified in the secret manifests by running the following command:
```bash
$ oc get secrets \
  -n openshift-image-registry installer-cloud-credentials \
  -o jsonpath='{.data}'
```
An output that contains the `azure_client_id` and `azure_federated_token_file` felids confirms that the components are assuming the Azure client ID.

- Azure clusters: Verify that the pod identity webhook is running by running the following command:
```bash
$ oc get pods \
  -n openshift-cloud-credential-operator
```
.Example output
```text
NAME                                         READY   STATUS    RESTARTS   AGE
cloud-credential-operator-59cf744f78-r8pbq   2/2     Running   2          71m
pod-identity-webhook-548f977b4c-859lz        1/1     Running   1          70m
```
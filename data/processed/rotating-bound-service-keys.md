ifdef::rotate-aws[= Rotating AWS OIDC bound service account signer keys]
ifdef::rotate-gcp[= Rotating Google Cloud OIDC bound service account signer keys]
ifdef::rotate-azure[= Rotating Azure OIDC bound service account signer keys]

If the Cloud Credential Operator (CCO) for your OpenShift Container Platform cluster
ifdef::rotate-aws[on Amazon Web Services (AWS)]
ifdef::rotate-gcp[on Google Cloud]
ifdef::rotate-azure[on Microsoft Azure]
is configured to operate in manual mode with
ifdef::rotate-aws[STS,]
ifdef::rotate-gcp[GCP Workload Identity,]
ifdef::rotate-azure[Microsoft Entra Workload ID,]
you can rotate the bound service account signer key.

To rotate the key, you delete the existing key on your cluster, which causes the Kubernetes API server to create a new key.
To reduce authentication failures during this process, you must immediately add the new public key to the existing issuer file.
After the cluster is using the new key for authentication, you can remove any remaining keys.

//Modified version of the disclaimer from enabling Azure WID on an existing cluster, since there are similar concerns:
> **IMPORTANT:** The process to rotate OIDC bound service account signer keys is disruptive and takes a significant amount of time. Some steps are time-sensitive. Before proceeding, observe the following considerations: * Read the following steps and ensure that you understand and accept the time requirement. The exact time requirement varies depending on the individual cluster, but it is likely to require at least one hour. * To reduce the risk of authentication failures, ensure that you understand and prepare for the time-sensitive steps. * During this process, you must refresh all service accounts and restart all pods on the cluster. These actions are disruptive to workloads. To mitigate this impact, you can temporarily halt these services and then redeploy them when the cluster is ready.

.Prerequisites

- You have access to the pass:quotes[OpenShift CLI (`oc`)] as a user with the `cluster-admin` role.

//Permissions requirements (per platform, for install and key rotation)

- You have configured the `ccoctl` utility.
- Your cluster is in a stable state.
You can confirm that the cluster is stable by running the following command:
```bash
$ oc adm wait-for-stable-cluster --minimum-stable-period=5s
```

.Procedure

1. Configure the following environment variables:
```text
```
> **NOTE:** Your cluster might differ from this example, and the resource names might not be derived identically from the cluster name. Ensure that you specify the correct corresponding resource names for your cluster.

1. Create a temporary directory to use and assign it an environment variable by running the following command:
```bash
$ TEMPDIR=$(mktemp -d)
```

1. To cause the Kubernetes API server to create a new bound service account signing key, you delete the next bound service account signing key.
> **IMPORTANT:** After you complete this step, the Kubernetes API server starts to roll out a new key. To reduce the risk of authentication failures, complete the remaining steps as quickly as possible. The remaining steps might be disruptive to workloads.
When you are ready, delete the next bound service account signing key by running the following command:
```bash
$ oc delete secrets/next-bound-service-account-signing-key \
  -n openshift-kube-apiserver-operator
```

1. Download the public key from the service account signing key secret that the Kubernetes API server created by running the following command:
```bash
$ oc get secret/next-bound-service-account-signing-key \
  -n openshift-kube-apiserver-operator \
  -ojsonpath='{ .data.service-account\.pub }' | base64 \
  -d > ${TEMPDIR}/serviceaccount-signer.public
```

1. Use the public key to create a `keys.json` file by running the following command:

1. Rename the `keys.json` file by running the following command:
```bash
$ cp ${TEMPDIR}/<number>-keys.json ${TEMPDIR}/jwks.new.json
```
where `<number>` is a two-digit numerical value that varies depending on your environment.

1. Download the existing `keys.json` file from the cloud provider by running the following command:

1. Combine the two `keys.json` files by running the following command:
```bash
$ jq -s '{ keys: map(.keys[])}' ${TEMPDIR}/jwks.current.json ${TEMPDIR}/jwks.new.json > ${TEMPDIR}/jwks.combined.json
```

1. To enable authentication for the old and new keys during the rotation, upload the combined `keys.json` file to the cloud provider by running the following command:

1. Wait for the Kubernetes API server to update and use the new key.
You can monitor the update progress by running the following command:
```bash
$ oc adm wait-for-stable-cluster
```
This process might take 15 minutes or longer.
The following output indicates that the process is complete:
```text
All clusteroperators are stable
```

1. To ensure that all pods on the cluster use the new key, you must restart them.
> **IMPORTANT:** This step maintains uptime for services that are configured for high availability across multiple nodes, but might cause downtime for any services that are not.
Restart all of the pods in the cluster by running the following command:
```bash
$ oc adm reboot-machine-config-pool mcp/worker mcp/master
```

1. Monitor the restart and update process by running the following command:
```bash
$ oc adm wait-for-node-reboot nodes --all
```
This process might take 15 minutes or longer.
The following output indicates that the process is complete:
```text
All nodes rebooted
```

1. Monitor the update progress by running the following command:
```bash
$ oc adm wait-for-stable-cluster
```
This process might take 15 minutes or longer.
The following output indicates that the process is complete:
```text
All clusteroperators are stable
```

1. Replace the combined `keys.json` file with the updated `keys.json` file on the cloud provider by running the following command:
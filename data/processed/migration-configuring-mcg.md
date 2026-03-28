# Retrieving Multicloud Object Gateway credentials

Retrieve the Multicloud Object Gateway (MCG) credentials and S3 endpoint, which you need to configure MCG as a replication repository for the Migration Toolkit for Containers (MTC).

Retrieve the Multicloud Object Gateway (MCG) credentials, which you need to create a `Secret` custom resource (CR) for MTC.

Retrieve the Multicloud Object Gateway (MCG) bucket credentials to create a `Secret` custom resource (CR) for OpenShift API for Data Protection (OADP).
//ifdef::installing-oadp-mcg[]
//endif::[]

> **NOTE:** Although the MCG Operator is link:https://catalog.redhat.com/software/containers/ocs4/mcg-rhel8-operator/5ddbcefbdd19c71643b56ce9?architecture=amd64&image=64243f5dcd0eb61355af9abd[deprecated], the MCG plugin is still available for OpenShift Data Foundation. To download the plugin, browse to link:https://access.redhat.com/downloads/content/547/ver=4/rhel---9/4.15.4/x86_64/product-software[Download Red Hat OpenShift Data Foundation] and download the appropriate MCG plugin for your operating system.

.Prerequisites
- You must deploy OpenShift Data Foundation by using the appropriate link:https://docs.redhat.com/en/documentation/red_hat_openshift_data_foundation/4.15[Red Hat OpenShift Data Foundation deployment guide].

.Procedure
- Obtain the S3 endpoint, `AWS_ACCESS_KEY_ID`, and the `AWS_SECRET_ACCESS_KEY` value by running the `oc describe` command for the `NooBaa` CR.
You use these credentials to add MCG as a replication repository.
1. Create an MCG bucket. For more information, see link:https://docs.redhat.com/en/documentation/red_hat_openshift_data_foundation/latest/html-single/managing_hybrid_and_multicloud_resources/index[Managing hybrid and multicloud resources].

1. Obtain the S3 endpoint, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and the bucket name by running the `oc describe` command on the bucket resource.

1. Create a `credentials-velero` file:
```bash
$ cat << EOF > ./credentials-velero
[default]
aws_access_key_id=<AWS_ACCESS_KEY_ID>
aws_secret_access_key=<AWS_SECRET_ACCESS_KEY>
EOF
```
You can use the `credentials-velero` file to create a `Secret` object when you install the Data Protection Application.
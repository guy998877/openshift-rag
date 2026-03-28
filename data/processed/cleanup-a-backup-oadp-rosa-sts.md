# Cleaning up a cluster after a backup with OADP and ROSA STS

If you need to uninstall the OpenShift API for Data Protection (OADP) Operator together with the backups and the S3 bucket from this example, follow these instructions.

.Procedure

1. Delete the workload by running the following command:
```bash
$ oc delete ns hello-world
```

1. Delete the Data Protection Application (DPA) by running the following command:
```bash
$ oc -n openshift-adp delete dpa ${CLUSTER_NAME}-dpa
```

1. Delete the cloud storage by running the following command:
```bash
$ oc -n openshift-adp delete cloudstorage ${CLUSTER_NAME}-oadp
```

> **WARNING:** If this command hangs, you might need to delete the finalizer by running the following command: [source,terminal] ---- $ oc -n openshift-adp patch cloudstorage ${CLUSTER_NAME}-oadp -p '{"metadata":{"finalizers":null}}' --type=merge ----

1. If the Operator is no longer required, remove it by running the following command:
```bash
$ oc -n openshift-adp delete subscription oadp-operator
```

1. Remove the namespace from the Operator:
```bash
$ oc delete ns openshift-adp
```

1. If the backup and restore resources are no longer required, remove them from the cluster by running the following command:
```bash
$ oc delete backups.velero.io hello-world
```

1. To delete backup, restore and remote objects in AWS S3 run the following command:
```bash
$ velero backup delete hello-world
```

1. If you no longer need the Custom Resource Definitions (CRD), remove them from the cluster by running the following command:
```bash
$ for CRD in `oc get crds | grep velero | awk '{print $1}'`; do oc delete crd $CRD; done
```

1. Delete the AWS S3 bucket by running the following commands:
```bash
$ aws s3 rm s3://${CLUSTER_NAME}-oadp --recursive
```
```bash
$ aws s3api delete-bucket --bucket ${CLUSTER_NAME}-oadp
```

1. Detach the policy from the role by running the following command:
```bash
$ aws iam detach-role-policy --role-name "${ROLE_NAME}"  --policy-arn "${POLICY_ARN}"
```

1. Delete the role by running the following command:
```bash
$ aws iam delete-role --role-name "${ROLE_NAME}"
```
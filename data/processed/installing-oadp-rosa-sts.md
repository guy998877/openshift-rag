# Installing the OADP Operator and providing the IAM role

AWS Security Token Service (AWS STS) is a global web service that provides short-term credentials for IAM or federated users. OpenShift Container Platform with STS is the recommended credential mode. This document describes how to install OpenShift API for Data Protection (OADP) on clusters with AWS STS.

> **IMPORTANT:** Restic is unsupported. Kopia file system backup (FSB) is supported when backing up file systems that do not support Container Storage Interface (CSI) snapshots. Example file systems include the following: * Amazon Elastic File System (EFS) * Network File System (NFS) * `emptyDir` volumes * Local volumes For backing up volumes, OADP on ROSA with AWS STS recommends native snapshots and Container Storage Interface (CSI) snapshots. Data Mover backups are supported, but can be slower than native snapshots. In an Amazon ROSA cluster that uses STS authentication, restoring backed-up data in a different AWS region is not supported.

.Prerequisites

- An OpenShift Container Platform 
cluster with the required access and tokens. For instructions, see the previous procedure _Preparing AWS credentials for OADP_. If you plan to use two different clusters for backing up and restoring, you must prepare AWS credentials, including `ROLE_ARN`, for each cluster.

.Procedure

1. Create 
an OpenShift Container Platform 
secret from your AWS token file by entering the following commands:

.. Create the credentials file:
```bash
$ cat <<EOF > ${SCRATCH}/credentials
  [default]
  role_arn = ${ROLE_ARN}
  web_identity_token_file = /var/run/secrets/openshift/serviceaccount/token
  region = <aws_region> # <1>
EOF
```
<1> Replace `<aws_region>` with the AWS region to use for the STS endpoint.
.. Create a namespace for OADP:
```bash
$ oc create namespace openshift-adp
```

.. Create the OpenShift Container Platform secret:
```bash
$ oc -n openshift-adp create secret generic cloud-credentials \
  --from-file=${SCRATCH}/credentials
```
> **NOTE:** In OpenShift Container Platform versions 4.15 and later, the OADP Operator supports a new standardized STS workflow through the Operator Lifecycle Manager (OLM) and Cloud Credentials Operator (CCO). In this workflow, you do not need to create the above secret, you only need to supply the role ARN during the installation of OLM-managed operators using the OpenShift Container Platform web console, for more information see _Installing from software catalog using the web console_. The preceding secret is created automatically by CCO.

1. Install the OADP Operator:
.. In the OpenShift Container Platform web console, browse to *Ecosystem* -> *Software Catalog*.
.. Search for the *OADP Operator*.
.. In the *role_ARN* field, paste the role_arn that you created previously and click *Install*.

1. Create AWS cloud storage using your AWS credentials by entering the following command:
```bash
$ cat << EOF | oc create -f -
  apiVersion: oadp.openshift.io/v1alpha1
  kind: CloudStorage
  metadata:
    name: ${CLUSTER_NAME}-oadp
    namespace: openshift-adp
  spec:
    creationSecret:
      key: credentials
      name: cloud-credentials
    enableSharedConfig: true
    name: ${CLUSTER_NAME}-oadp
    provider: aws
    region: $REGION
EOF
```
// bringing over from MOB docs
1. Check your application's storage default storage class by entering the following command:
```bash
$ oc get pvc -n <namespace>
```

.Example output

```bash
NAME     STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
applog   Bound    pvc-351791ae-b6ab-4e8b-88a4-30f73caf5ef8   1Gi        RWO            gp3-csi        4d19h
mysql    Bound    pvc-16b8e009-a20a-4379-accc-bc81fedd0621   1Gi        RWO            gp3-csi        4d19h
```

1. Get the storage class by running the following command:
```bash
$ oc get storageclass
```

.Example output
```bash
NAME                PROVISIONER             RECLAIMPOLICY   VOLUMEBINDINGMODE      ALLOWVOLUMEEXPANSION   AGE
gp2                 kubernetes.io/aws-ebs   Delete          WaitForFirstConsumer   true                   4d21h
gp2-csi             ebs.csi.aws.com         Delete          WaitForFirstConsumer   true                   4d21h
gp3                 ebs.csi.aws.com         Delete          WaitForFirstConsumer   true                   4d21h
gp3-csi (default)   ebs.csi.aws.com         Delete          WaitForFirstConsumer   true                   4d21h
```
> **NOTE:** The following storage classes will work: * gp3-csi * gp2-csi * gp3 * gp2
If the application or applications that are being backed up are all using persistent volumes (PVs) with Container Storage Interface (CSI), it is advisable to include the CSI plugin in the OADP DPA configuration.

1. Create the `DataProtectionApplication` resource to configure the connection to the storage where the backups and volume snapshots are stored:

.. If you are using only CSI volumes, deploy a Data Protection Application by entering the following command:
```bash
$ cat << EOF | oc create -f -
  apiVersion: oadp.openshift.io/v1alpha1
  kind: DataProtectionApplication
  metadata:
    name: ${CLUSTER_NAME}-dpa
    namespace: openshift-adp
  spec:
    backupImages: true # <1>
    features:
      dataMover:
        enable: false
    backupLocations:
    - bucket:
        cloudStorageRef:
          name: ${CLUSTER_NAME}-oadp
        credential:
          key: credentials
          name: cloud-credentials
        prefix: velero
        default: true
        config:
          region: ${REGION}
    configuration:
      velero:
        defaultPlugins:
        - openshift
        - aws
        - csi
      nodeAgent:  # <2>
        enable: false
        uploaderType: kopia # <3>
EOF
```
<1> ROSA supports internal image backup. Set this field to `false` if you do not want to use image backup.
<2> See the important note regarding the `nodeAgent` attribute at the end of this procedure.
<3> The type of uploader. The built-in Data Mover uses Kopia as the default uploader mechanism regardless of the value of the `uploaderType` field.
// . Create the `DataProtectionApplication` resource, which is used to configure the connection to the storage where the backups and volume snapshots are stored:

.. If you are using CSI or non-CSI volumes, deploy a Data Protection Application by entering the following command:
```bash
$ cat << EOF | oc create -f -
  apiVersion: oadp.openshift.io/v1alpha1
  kind: DataProtectionApplication
  metadata:
    name: ${CLUSTER_NAME}-dpa
    namespace: openshift-adp
  spec:
    backupImages: true # <1>
    backupLocations:
    - bucket:
        cloudStorageRef:
          name: ${CLUSTER_NAME}-oadp
        credential:
          key: credentials
          name: cloud-credentials
        prefix: velero
        default: true
        config:
          region: ${REGION}
    configuration:
      velero:
        defaultPlugins:
        - openshift
        - aws
      nodeAgent: # <2>
        enable: false
        uploaderType: restic
    snapshotLocations:
      - velero:
          config:
            credentialsFile: /tmp/credentials/openshift-adp/cloud-credentials-credentials # <3>
            enableSharedConfig: "true" # <4>
            profile: default # <5>
            region: ${REGION} # <6>
          provider: aws
EOF
```
<1> ROSA supports internal image backup. Set this field to `false` if you do not want to use image backup.
<2> See the important note regarding the `nodeAgent` attribute at the end of this procedure.
<3> The `credentialsFile` field is the mounted location of the bucket credential on the pod.
<4> The `enableSharedConfig` field allows the `snapshotLocations` to share or reuse the credential defined for the bucket.
<5> Use the profile name set in the AWS credentials file.
<6> Specify `region` as your AWS region. This must be the same as the cluster region.
You are now ready to back up and restore OpenShift Container Platform applications, as described in _Backing up applications_.

> **IMPORTANT:** The `enable` parameter of `restic` is set to `false` in this configuration, because OADP does not support Restic in ROSA environments. If you use OADP 1.2, replace this configuration: [source,terminal] ---- nodeAgent: enable: false uploaderType: restic ---- with the following configuration: [source,terminal] ---- restic: enable: false ----

If you want to use two different clusters for backing up and restoring, the two clusters must have the same AWS S3 storage names in both the cloud storage CR and the OADP `DataProtectionApplication` configuration.
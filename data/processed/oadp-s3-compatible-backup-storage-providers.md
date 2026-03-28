# AWS S3 compatible backup storage providers

OADP works with many S3-compatible object storage providers. Several object storage providers are certified and tested with every release of OADP. Various S3 providers are known to work with OADP but are not specifically tested and certified. These providers will be supported on a best-effort basis. Additionally, there are a few S3 object storage providers with known issues and limitations that are listed in this documentation.

> **NOTE:** Red Hat will provide support for OADP on any S3-compatible storage, but support will stop if the S3 endpoint is determined to be the root cause of an issue.

## Certified backup storage providers

The following AWS S3 compatible object storage providers are fully supported by OADP through the AWS plugin for use as backup storage locations:

- MinIO
- Multicloud Object Gateway (MCG)
- Amazon Web Services (AWS) S3
- IBM Cloud(R) Object Storage S3
- Ceph RADOS Gateway (Ceph Object Gateway)
- Red Hat Container Storage
- Red Hat OpenShift Data Foundation
- NetApp ONTAP S3 Object Storage
- link:https://downloads.scality.com/artesca-ova/doc/general_introduction.html#[Scality ARTESCA S3 object storage]

> **NOTE:** The following compatible object storage providers are supported and have their own Velero object store plugins: * Google Cloud * Microsoft Azure

## Unsupported backup storage providers

The following AWS S3 compatible object storage providers, are known to work with Velero through the AWS plugin, for use as backup storage locations, however, they are unsupported and have not been tested by Red Hat:

- Oracle Cloud
- DigitalOcean
- NooBaa, unless installed using Multicloud Object Gateway (MCG)
- Tencent Cloud
- Quobyte
- Cloudian HyperStore

## Backup storage providers with known limitations

The following AWS S3 compatible object storage providers are known to work with Velero through the AWS plugin with a limited feature set:

- Swift - It works for use as a backup storage location for backup storage, but is not compatible with Restic for filesystem-based volume backup and restore.
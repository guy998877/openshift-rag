# Indicating that the cluster is ready to upgrade

The Cloud Credential Operator (CCO) `Upgradable` status for a cluster with manually maintained credentials is `False` by default.

.Prerequisites

- For the release image that you are upgrading to, you have processed any new credentials manually or by using the Cloud Credential Operator utility (`ccoctl`).
- You have installed the OpenShift CLI (`oc`).

.Procedure

1. Log in to `oc` on the cluster as a user with the `cluster-admin` role.

1. Edit the `CloudCredential` resource to add an `upgradeable-to` annotation within the `metadata` field by running the following command:
```bash
$ oc edit cloudcredential cluster
```
.Text to add
```yaml
...
  metadata:
    annotations:
      cloudcredential.openshift.io/upgradeable-to: <version_number>
...
```
Where `<version_number>` is the version that you are upgrading to, in the format `x.y.z`. For example, use `4.12.2` for OpenShift Container Platform 4.12.2.
It may take several minutes after adding the annotation for the upgradeable status to change.

.Verification

//Would like to add CLI steps for same
1. In the *Administrator* perspective of the web console, navigate to *Administration* -> *Cluster Settings*.

1. To view the CCO status details, click *cloud-credential* in the *Cluster Operators* list.
--
- If the *Upgradeable* status in the *Conditions* section is *False*, verify that the `upgradeable-to` annotation is free of typographical errors.
--

1. When the *Upgradeable* status in the *Conditions* section is *True*, begin the OpenShift Container Platform upgrade.
# Creating an Object Bucket Claim for disaster recovery on OpenShift Data Foundation

If you use cluster storage for your Multicloud Object Gateway (MCG) bucket `backupStorageLocation` on OpenShift Data Foundation, create an Object Bucket Claim (OBC) using the OpenShift Web Console.

> **WARNING:** Failure to configure an Object Bucket Claim (OBC) might lead to backups not being available.

.Procedure

- Create an Object Bucket Claim (OBC) using the OpenShift web console as described in link:https://access.redhat.com/documentation/en-us/red_hat_openshift_data_foundation/4.13/html/managing_hybrid_and_multicloud_resources/object-bucket-claim#creating-an-object-bucket-claim-using-the-openshift-web-console_rhodf[Creating an Object Bucket Claim using the OpenShift Web Console].
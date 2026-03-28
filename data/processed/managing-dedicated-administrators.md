# Managing OpenShift Container Platform administrators

Administrator roles are managed using a `cluster-admin` or `dedicated-admin` group on the cluster. Existing members of this group can edit membership through [OpenShift Cluster Manager](https://console.redhat.com/openshift).

.Procedure

1. Navigate to the *Cluster Details* page and select the *Access Control* tab.
1. Select the *Cluster Roles and Access* tab and click *Add user*.
1. Enter the user name and select your group.
1. Click *Add user*.
> **NOTE:** Adding a user to the `cluster-admin` group can take several minutes to complete.
1. Optional: To remove a OpenShift Container Platform administrator, click the Options menu image:kebab.png[title="Options menu"] to the right of the user and group combination and click *Delete*.
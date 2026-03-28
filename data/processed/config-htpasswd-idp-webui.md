# Configuring an htpasswd identity provider

You can create an htpasswd identity provider with the OpenShift Cluster Manager web user interface (UI).

.Procedure

1. Select your cluster from the the *Cluster List* page on link:https://console.redhat.com/openshift[OpenShift Cluster Manager].

1. Select *Access control* -> *Identity providers*.

1. Click *Add identity provider*.

1. Select *HTPasswd* from the *Identity Provider* list.

1. Add a unique name in the *Name* field for the identity provider.

1. Use the suggested username and password for the static user, or create your own.
> **NOTE:** You cannot retrieve the credentials defined in this step after you select *Add* in the following step. If you lose the credentials, you must recreate the identity provider and define the credentials again.

1. Select *Add* to create the htpasswd identity provider and the single, static user.

1. Grant the static user permission to manage the cluster:
.. Select *Access control* -> *Cluster Roles and Access* > *Add user*.
.. Enter the User ID of the static user that you created in the preceding step.
.. Select *Add user* to grant the administration privileges to the user.

.Verification

- The configured htpasswd identity provider is visible on the *Access control* -> *Identity providers* page.
> **NOTE:** After creating the identity provider, synchronization usually completes within two minutes. You can log in to the cluster as the user after the htpasswd identity provider becomes available.
- The single, administrative user is visible on the *Access control* -> *Cluster Roles and Access* page. The administration group membership of the user is also displayed.
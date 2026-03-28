# How OADP Self-Service works

Review how OADP Self-Service processes backup requests through the `NonAdminController` (NAC) custom resource, which validates namespace administrator requests and creates corresponding `Velero` backup objects.

The diagram describes the following workflow:

1. A namespace admin user creates a `NonAdminBackup` (NAB) custom resource (CR) request.
1. The `NonAdminController` (NAC) CR receives the NAB CR request.
1. The NAC validates the request and updates the NAB CR about the request.
1. The NAC creates the `Velero` backup object.
1. The NAC monitors the `Velero` backup object and cascades the status back to the NAB CR. 

.How OADP Self-Service works
image::oadp-self-service.svg[OADP Self-Service]
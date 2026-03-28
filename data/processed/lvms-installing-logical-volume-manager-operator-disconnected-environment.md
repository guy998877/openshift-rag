# Installing LVM Storage in a disconnected environment

You can install LVM Storage on OpenShift Container Platform in a disconnected environment. All sections referenced in this procedure are linked in the "Additional resources" section.

.Prerequisites

- You read the "About disconnected installation mirroring" section.
- You have access to the OpenShift Container Platform image repository.
- You created a mirror registry.

.Procedure

1. Follow the steps in the "Creating the image set configuration" procedure. To create an `ImageSetConfiguration` custom resource (CR) for LVM Storage, you can use the following example `ImageSetConfiguration` CR configuration:

1. Follow the procedure in the "Mirroring an image set to a mirror registry" section.

1. Follow the procedure in the "Configuring image registry repository mirroring" section.
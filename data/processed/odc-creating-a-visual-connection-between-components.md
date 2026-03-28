# Creating a visual connection between components

You can depict an intent to connect application components by using the visual connector.

This procedure walks you through an example of creating a visual connection between a PostgreSQL Database service and a Spring PetClinic sample application.

.Prerequisites

- You have created and deployed a Spring PetClinic sample application by using the *Developer* perspective.
- You have created and deployed a Crunchy PostgreSQL database instance by using the *Developer* perspective. This instance has the following components: `hippo-backup`, `hippo-instance`, `hippo-repo-host`, and  `hippo-pgbouncer`.

.Procedure

1. In the *Developer* perspective, switch to the relevant project, for example, `my-petclinic`.

1. Hover over the Spring PetClinic sample application to see a dangling arrow on the node.
.Visual connector
image::odc_connector.png[]
1. Click and drag the arrow towards the `hippo-pgbouncer` deployment to connect the Spring PetClinic sample application with it.
1. Click the `spring-petclinic` deployment to see the *Overview* panel. Under the *Details* tab, click the edit icon in the *Annotations* section to see the *Key = `app.openshift.io/connects-to`* and *Value = `[{"apiVersion":"apps/v1","kind":"Deployment","name":"hippo-pgbouncer"}]`* annotation added to the deployment.

1. Optional: You can repeat these steps to establish visual connections between other applications and components you create.
.Connecting multiple applications
image::odc_connecting_multiple_applications.png[]
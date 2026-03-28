# Creating a binding connection between components

You can create a binding connection with Operator-backed components, as demonstrated in the following example, which uses a PostgreSQL Database service and a Spring PetClinic sample application. To create a binding connection with a service that the PostgreSQL Database Operator backs, you must first add the Red Hat-provided PostgreSQL Database Operator to the *OperatorHub*, and then install the Operator. The PostreSQL Database Operator then creates and manages the Database resource, which exposes the binding data in secrets, config maps, status, and spec attributes.

.Prerequisites

- You created and deployed a Spring PetClinic sample application in the *Developer* perspective.
- You installed {servicebinding-title} from the software catalog.
- You installed the *Crunchy Postgres for Kubernetes* Operator from the software catalog in the `v5` *Update* channel.
- You created a *PostgresCluster* resource in the *Developer* perspective, which resulted in a Crunchy PostgreSQL database instance with the following components: `hippo-backup`, `hippo-instance`, `hippo-repo-host`, and `hippo-pgbouncer`.

.Procedure

1. In the *Developer* perspective, switch to the relevant project, for example, `my-petclinic`.
1. In the *Topology* view, hover over the Spring PetClinic sample application to see a dangling arrow on the node.
1. Drag and drop the arrow onto the *hippo* database icon in the Postgres Cluster to make a binding connection with the Spring PetClinic sample application.

1. In the *Create Service Binding* dialog, keep the default name or add a different name for the service binding, and then click *Create*.
.Service Binding dialog
image::odc-sbc-modal.png[]
1. Optional: If there is difficulty in making a binding connection using the Topology view, go to *+Add* -> *YAML* -> *Import YAML*.
1. Optional: In the YAML editor, add the `ServiceBinding` resource:
```yaml
apiVersion: binding.operators.coreos.com/v1alpha1
kind: ServiceBinding
metadata:
    name: spring-petclinic-pgcluster
    namespace: my-petclinic
spec:
    services:
    - group: postgres-operator.crunchydata.com
      version: v1beta1
      kind: PostgresCluster
      name: hippo
    application:
      name: spring-petclinic
      group: apps
      version: v1
      resource: deployments
```
A service binding request is created and a binding connection is created through a `ServiceBinding` resource. When the database service connection request succeeds, the application is redeployed and the connection is established.
.Binding connector
image::odc-binding-connector.png[]
> **TIP:** You can also use the context menu by dragging the dangling arrow to add and create a binding connection to an operator-backed service. .Context menu to create binding connection image::odc_context_operator.png[]

1. In the navigation menu, click *Topology*. The spring-petclinic deployment in the Topology view includes an Open URL link to view its web page.

1. Click the *Open URL* link.

You can now view the Spring PetClinic sample application remotely to confirm that the application is now connected to the database service and that the data has been successfully projected to the application from the Crunchy PostgreSQL database service.

The Service Binding Operator has successfully created a working connection between the application and the database service.
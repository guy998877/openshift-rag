# Creating applications by deploying container image

You can use an external image registry or an image stream tag from an internal registry to deploy an application on your cluster.

.Prerequisites

- You have logged in to the OpenShift Container Platform web console and are in the *Developer* perspective.

.Procedure

1. In the *+Add* view, click *Container images* to view the *Deploy Images* page.
1. In the *Image* section:
.. Select *Image name from external registry* to deploy an image from a public or a private registry, or select *Image stream tag from internal registry* to deploy an image from an internal registry.
.. Select an icon for your image in the *Runtime icon* tab.
1. In the *General* section:
.. In the *Application name* field, enter a unique name for the application grouping.
.. In the *Name* field, enter a unique name to identify the resources created for this component.
1. In the *Resource type* section, select the resource type to generate:
.. Select *Deployment* to enable declarative updates for `Pod` and `ReplicaSet` objects.
.. Select *DeploymentConfig* to define the template for a `Pod` object, and manage deploying new images and configuration sources.
.. Select *Serverless Deployment* to enable scaling to zero when idle.
1. Click *Create*. You can view the build status of the application in the *Topology* view.
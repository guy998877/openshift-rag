# Deploying a Java application by uploading a JAR file

You can use the web console *Developer* perspective to upload a JAR file by using the following options:

- Navigate to the *+Add* view of the *Developer* perspective, and click *Upload JAR file* in the *From Local Machine* tile. Browse and select your JAR file, or drag a JAR file to deploy your application.

- Navigate to the *Topology* view and use the *Upload JAR file* option, or drag a JAR file to deploy your application.

- Use the in-context menu in the *Topology* view, and then use the *Upload JAR file* option to upload your JAR file to deploy your application.

.Prerequisites

- The Cluster Samples Operator must be installed by a cluster administrator.
- You have access to the OpenShift Container Platform web console and are in the *Developer* perspective.

.Procedure

1. In the *Topology* view, right-click anywhere to view the *Add to Project* menu.

1. Hover over the *Add to Project* menu to see the menu options, and then select the *Upload JAR file* option to see the *Upload JAR file* form. Alternatively, you can drag the JAR file into the *Topology* view.

1. In the *JAR file* field, browse for the required JAR file on your local machine and upload it. Alternatively, you can drag the JAR file on to the field. A toast alert is displayed at the top right if an incompatible file type is dragged into the *Topology* view. A field error is displayed if an incompatible file type is dropped on the field in the upload form.

1. The runtime icon and builder image are selected by default. If a builder image is not auto-detected, select a builder image. If required, you can change the version using the *Builder Image Version* drop-down list.

1. Optional: In the *Application Name* field, enter a unique name for your application to use for resource labelling.

1. In the *Name* field, enter a unique component name for the associated resources.

1. Optional: Use the *Resource type* drop-down list to change the resource type.

1. In the *Advanced options* menu, click *Create a Route to the Application* to configure a public URL for your deployed application.

1. Click *Create* to deploy the application. A toast notification is shown to notify you that the JAR file is being uploaded. The toast notification also includes a link to view the build logs.

> **NOTE:** If you attempt to close the browser tab while the build is running, a web alert is displayed.

After the JAR file is uploaded and the application is deployed, you can view the application in the *Topology* view.
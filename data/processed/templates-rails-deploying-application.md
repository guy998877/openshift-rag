# Deploying your application to OpenShift Container Platform

You can deploy you application to OpenShift Container Platform.

After creating the `rails-app` project, you are automatically switched to the new project namespace.

Deploying your application in OpenShift Container Platform involves three steps:

- Creating a database service from OpenShift Container Platform's PostgreSQL image.
- Creating a frontend service from OpenShift Container Platform's Ruby 2.0 builder image and
your Ruby on Rails source code, which are wired with the database service.
- Creating a route for your application.

.Procedure
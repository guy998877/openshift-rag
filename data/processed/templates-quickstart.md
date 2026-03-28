# Quick start templates

A quick start template is a basic example of an application running on OpenShift Container Platform. Quick starts come in a variety of languages and frameworks, and are defined in a template, which is constructed from a set of services, build configurations, and deployment configurations. This template references the necessary images and source repositories to build and deploy the application.

To explore a quick start, create an application from a template. Your administrator must have already installed these templates in your OpenShift Container Platform cluster, in which case you can simply select it from the web console.

Quick starts refer to a source repository that contains the application source code. To customize the quick start, fork the repository and, when creating an application from the template, substitute the default source repository name with your forked repository. This results in builds that are performed using your source code instead of the provided example source. You can then update the code in your source repository and launch a new build to see the changes reflected in the deployed application.

## Web framework quick start templates

These quick start templates provide a basic application of the indicated framework and language:

- CakePHP: a PHP web framework that includes a MySQL database
- Dancer: a Perl web framework that includes a MySQL database
- Django: a Python web framework that includes a PostgreSQL database
- NodeJS: a NodeJS web application that includes a MongoDB database
- Rails: a Ruby web framework that includes a PostgreSQL database

//* CakePHP: a PHP web framework (includes a MySQL database)
//** [Template definition](https://github.com/openshift/origin/tree/master/examples/quickstarts/cakephp-mysql.json)
//** [Source repository](https://github.com/sclorg/cakephp-ex)
//* Dancer: a Perl web framework (includes a MySQL database)
//** [Template definition](https://github.com/openshift/origin/tree/master/examples/quickstarts/dancer-mysql.json)
//** [Source repository](https://github.com/sclorg/dancer-ex)
//* Django: a Python web framework (includes a PostgreSQL database)
//** [Template definition](https://github.com/openshift/origin/tree/master/examples/quickstarts/django-postgresql.json)
//** [Source repository](https://github.com/sclorg/django-ex)
//* NodeJS: a NodeJS web application (includes a MongoDB database)
//** [Template definition](https://github.com/openshift/origin/tree/master/examples/quickstarts/nodejs-mongodb.json)
//** [Source repository](https://github.com/sclorg/nodejs-ex)
//* Rails: a Ruby web framework (includes a PostgreSQL database)
//** [Template definition](https://github.com/openshift/origin/tree/master/examples/quickstarts/rails-postgresql.json)
//** [Source repository](https://github.com/sclorg/rails-ex)
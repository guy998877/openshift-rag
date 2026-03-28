# Creating the frontend service

To bring your application to OpenShift Container Platform, you must specify a repository in which your application lives.

.Procedure

1. Create the frontend service and specify database related environment variables that were setup when creating the database service:
```bash
$ oc new-app path/to/source/code --name=rails-app -e POSTGRESQL_USER=username -e POSTGRESQL_PASSWORD=password -e POSTGRESQL_DATABASE=db_name -e DATABASE_SERVICE_NAME=postgresql
```
With this command, OpenShift Container Platform fetches the source code, sets up the builder, builds your application image, and deploys the newly created image together with the specified environment variables. The application is named `rails-app`.

1. Verify the environment variables have been added by viewing the JSON document of the `rails-app` deployment config:
```bash
$ oc get dc rails-app -o json
```
You should see the following section:
.Example output
```json
env": [
    {
        "name": "POSTGRESQL_USER",
        "value": "username"
    },
    {
        "name": "POSTGRESQL_PASSWORD",
        "value": "password"
    },
    {
        "name": "POSTGRESQL_DATABASE",
        "value": "db_name"
    },
    {
        "name": "DATABASE_SERVICE_NAME",
        "value": "postgresql"
    }

],
```

1. Check the build process:
```bash
$ oc logs -f build/rails-app-1
```

1. After the build is complete, look at the running pods in OpenShift Container Platform:
```bash
$ oc get pods
```
You should see a line starting with `myapp-<number>-<hash>`, and that is your application running in OpenShift Container Platform.

1. Before your application is functional, you must initialize the database by running the database migration script. There are two ways you can do this:
- Manually from the running frontend container:
- Exec into frontend container with `rsh` command:
```bash
$ oc rsh <frontend_pod_id>
```
- Run the migration from inside the container:
```bash
$ RAILS_ENV=production bundle exec rake db:migrate
```
If you are running your Rails application in a `development` or `test` environment you do not have to specify the `RAILS_ENV` environment variable.
- By adding pre-deployment lifecycle hooks in your template.
# Viewing a deployment

You can view a deployment to get basic information about all the available revisions of your application.

.Procedure

1. To show details about all recently created replication controllers for the provided `DeploymentConfig` object, including any currently running deployment process, run the following command:
```bash
$ oc rollout history dc/<name>
```

1. To view details specific to a revision, add the `--revision` flag:
```bash
$ oc rollout history dc/<name> --revision=1
```

1. For more detailed information about a `DeploymentConfig` object and its latest revision, use the `oc describe` command:
```bash
$ oc describe dc <name>
```
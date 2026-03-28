# Viewing deployment logs

.Procedure

1. To stream the logs of the latest revision for a given `DeploymentConfig` object:
```bash
$ oc logs -f dc/<name>
```
If the latest revision is running or failed, the command returns the logs of the process that is responsible for deploying your pods. If it is successful, it returns the logs from a pod of your application.

1. You can also view logs from older failed deployment processes, if and only if these processes (old replication controllers and their deployer pods) exist and have not been pruned or deleted manually:
```bash
$ oc logs --version=1 dc/<name>
```
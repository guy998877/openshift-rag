# Changing the update server by using the CLI

You can change the update server your cluster uses to retrieve information about update paths.

Changing the update server is optional. If you have an OpenShift Update Service (OSUS) installed and configured locally, you must set the URL for the server as the `upstream` to use the local server during updates. The default value for `upstream` is `\https://api.openshift.com/api/upgrades_info/v1/graph`.

.Procedure

- Change the `upstream` parameter value in the cluster version by running the following command:
```bash
$ oc patch clusterversion/version --patch '{"spec":{"upstream":"<update_server_url>"}}' --type=merge
```
Replace `<update_server_url>` with the URL for the update server.
.Example output
```bash
clusterversion.config.openshift.io/version patched
```
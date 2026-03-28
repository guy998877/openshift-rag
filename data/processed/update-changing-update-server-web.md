# Changing the update server by using the web console

Changing the update server is optional. If you have an OpenShift Update Service (OSUS) installed and configured locally, you must set the URL for the server as the `upstream` to use the local server during updates.

.Prerequisites
- You have access to the cluster with `cluster-admin` privileges.

- You have access to the OpenShift Container Platform web console.

.Procedure

1. Navigate to *Administration* -> *Cluster Settings*, click *version*.
1. Click the *YAML* tab and then edit the `upstream` parameter value:
.Example output
```yaml
  ...
  spec:
    clusterID: db93436d-7b05-42cc-b856-43e11ad2d31a
    upstream: '<update-server-url>' <1>
  ...
```
<1> The `<update-server-url>` variable specifies the URL for the update server.
The default `upstream` is `\https://api.openshift.com/api/upgrades_info/v1/graph`.

1. Click *Save*.
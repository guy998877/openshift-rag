# Disabling overcommitment for a project

If overcommitment is enabled on a project, you can disable overcommitment for that projects. This allows infrastructure components to be configured independently of overcommitment.

.Procedure
//For OCP and Origin:
1. Create or edit the namespace object file.
1. Add the following annotation:
//For ROSA, ROSA-HCP, OSD:
.. If you are using the OpenShift CLI (`oc`):
... Edit the namespace:
```bash
$ oc edit namespace/<project_name>
```
```yaml
apiVersion: v1
kind: Namespace
metadata:
  annotations:
    quota.openshift.io/cluster-resource-override-enabled: "false"
# ...
```
where:
--
`metadata.annotations.quota.openshift.io/cluster-resource-override-enabled.false`:: Specifies that overcommit is disabled for this namespace.
--
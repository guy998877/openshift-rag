# Creating custom resources from a file

After a custom resource definition (CRD) has been added to the cluster, custom resources (CRs) can be created with the CLI from a file using the CR specification.

.Prerequisites

.Procedure

1. Create a YAML file for the CR. In the following example definition, the `cronSpec` and `image` custom fields are set in a CR of `Kind: CronTab`. The `Kind` comes from the `spec.kind` field of the CRD object:
.Example YAML file for a CR
```yaml
apiVersion: "stable.example.com/v1" <1>
kind: CronTab <2>
metadata:
  name: my-new-cron-object <3>
  finalizers: <4>
  - finalizer.stable.example.com
spec: <5>
  cronSpec: "* * * * /5"
  image: my-awesome-cron-image
```
<1> Specify the group name and API version (name/version) from the CRD.
<2> Specify the type in the CRD.
<3> Specify a name for the object.
<4> Specify the [finalizers](https://kubernetes.io/docs/tasks/access-kubernetes-api/extend-api-custom-resource-definitions/#finalizers) for the object, if any. Finalizers allow controllers to implement conditions that must be completed before the object can be deleted.
<5> Specify conditions specific to the type of object.

1. After you create the file, create the object:
```bash
$ oc create -f <file_name>.yaml
```
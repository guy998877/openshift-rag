# Listing volumes and volume mounts in a pod

You can list volumes and volume mounts in pods or pod templates:

.Procedure

To list volumes:

```bash
$ oc set volume <object_type>/<name> [options]
```

List volume supported options:
[cols="3a*",options="header"]
|===

|Option |Description |Default

|`--name`
|Name of the volume.
|

|`-c, --containers`
|Select containers by name. It can also take wildcard `'*'` that matches any
character.
|`'*'`
|===

For example:

- To list all volumes for pod *p1*:
```bash
$ oc set volume pod/p1
```

- To list volume *v1* defined on all deployment configs:
```bash
$ oc set volume dc --all --name=v1
```
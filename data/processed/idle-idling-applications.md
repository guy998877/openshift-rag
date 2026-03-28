# Idling applications

Idling an application involves finding the scalable resources (deployment
configurations, replication controllers, and others) associated with a service.
Idling an application finds the service and marks it as idled, scaling down the
resources to zero replicas.

You can use the `oc idle` command to idle a single service, or use the
`--resource-names-file` option to idle multiple services.

## Idling a single service

.Procedure

1. To idle a single service, run:
```bash
$ oc idle <service>
```

## Idling multiple services

Idling multiple services is helpful if an application spans across a set of
services within a project, or when idling multiple services in conjunction with
a script to idle multiple applications in bulk within the same project.

.Procedure

1. Create a file containing a list of the services, each on their own line.

1. Idle the services using the `--resource-names-file` option:
```bash
$ oc idle --resource-names-file <filename>
```

> **NOTE:** The `idle` command is limited to a single project. For idling applications across a cluster, run the `idle` command for each project individually.
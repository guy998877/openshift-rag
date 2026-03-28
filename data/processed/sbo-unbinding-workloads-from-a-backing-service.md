# Unbinding workloads from a backing service

You can unbind a workload from a backing service by using the `oc` tool.

- To unbind a workload from a backing service, delete the `ServiceBinding` custom resource (CR) linked to it:
```bash
$ oc delete ServiceBinding <.metadata.name>
```
.Example
```bash
$ oc delete ServiceBinding spring-petclinic-pgcluster
```
where:
[horizontal]
`spring-petclinic-pgcluster`:: Specifies the name of the `ServiceBinding` CR.
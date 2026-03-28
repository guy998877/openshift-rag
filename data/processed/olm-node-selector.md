# Overriding the node selector for catalog source pods

.Prerequisites

- A `CatalogSource` object of source type `grpc` with `spec.image` is defined.

.Procedure

- Edit the `CatalogSource` object and add or modify the `spec.grpcPodConfig` section to include the following:
```yaml
  grpcPodConfig:
    nodeSelector:
      custom_label: <label>
```
where `<label>` is the label for the node selector that you want catalog source pods to use for scheduling.
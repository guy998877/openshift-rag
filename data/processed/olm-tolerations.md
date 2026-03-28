# Overriding tolerations for catalog source pods

.Prerequisites

- A `CatalogSource` object of source type `grpc` with `spec.image` is defined.

.Procedure

- Edit the `CatalogSource` object and add or modify the `spec.grpcPodConfig` section to include the following:
```yaml
  grpcPodConfig:
    tolerations:
      - key: "<key_name>"
        operator: "<operator_type>"
        value: "<value>"
        effect: "<effect>"
```
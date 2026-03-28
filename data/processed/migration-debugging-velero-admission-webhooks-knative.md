# Restoring Knative resources

Resolve issues with restoring Knative resources that use admission webhooks by restoring the top-level `service.serving.knative.dev` service resource with Velero. This helps you to ensure that Knative resources are restored successfully without admission webhook errors.

.Procedure

- Restore the top level `service.serving.knative.dev Service` resource by using the following command:
```bash
$ velero restore <restore_name> \
  --from-backup=<backup_name> --include-resources \
  service.serving.knative.dev
```
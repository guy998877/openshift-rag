# Workaround for OpenShift ADP Controller segmentation fault

Define either `velero` or `cloudstorage` in your Data Protection Application (DPA) configuration to prevent indefinite pod crashes. This configuration resolves a segmentation fault in the `openshift-adp-controller-manager` pod that occurs when both components are enabled.

Define either `velero` or `cloudstorage` when you configure a DPA. Otherwise, the `openshift-adp-controller-manager` pod fails with a crash loop segmentation fault due to the following settings:

- If you define both `velero` and `cloudstorage`, the `openshift-adp-controller-manager` fails.
- If you do not define both `velero` and `cloudstorage`, the `openshift-adp-controller-manager` fails.

For more information about this issue, see [OADP-1054](https://issues.redhat.com/browse/OADP-1054).
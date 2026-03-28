# Deploying a {FeatureName}

To deploy a {FeatureName}, you create an instance of the `{FeatureResourceName}` resource.

.Procedure

1. Create a YAML file for a `{FeatureResourceName}` resource that contains the custom resource definition.

1. Create the custom resource in the cluster by running the following command:
```bash
$ oc create -f <filename>.yaml
```
where:

<filename>:: Specifies the name of the YAML file you created.

// Undefine attributes, so that any mistakes are easily spotted
:!FeatureName:
:!FeatureResourceName:
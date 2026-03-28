# Accessing private repositories from DeploymentConfig objects

You can add a secret to your `DeploymentConfig` object so that it can access images from a private repository. This procedure shows the OpenShift Container Platform web console method.

.Procedure

1. Create a new project.

1. Navigate to *Workloads* -> *Secrets*. 

1. Create a secret that contains credentials for accessing a private image repository.

1. Navigate to *Workloads* -> *DeploymentConfigs*. 

1. Create a `DeploymentConfig` object.

1. On the `DeploymentConfig` object editor page, set the *Pull Secret* and save your changes.
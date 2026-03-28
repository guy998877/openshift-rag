# Changing seLinuxChangePolicy at the pod level

You can set the set the `seLinuxChangePolicy` parameter in a new or existing Deployment, and then the pods that it manages will have this parameter value. You can similarly do this for a StatefulSet. You cannot edit an existing pod to set `seLinuxChangePolicy`; however, you can set this parameter when creating a new pod.

This procedure describes how to set the `seLinuxChangePolicy` parameter in an existing deployment.

.Prerequisites

- Access to the OpenShift Container Platform console.

.Procedure

To set the `seLinuxChangePolicy` parameter in an existing deployment:

1. Click *Workloads* > *Deployments*.

1. On the *Deployment* page, click the desired deployment.

1. On the *Deployment details* page, click the *YAML* tab.

1. Edit the deployment's YAML file under `spec.template.spec.securityContext` as per the following example file:
.Example deployment YAML file setting `seLinuxChangePolicy`
```yaml
  ...
securityContext:
  seLinuxChangePolicy: Recursive <1>
  ...
```
<1> Specifies recursively relabeling all files on all pod volumes to the appropriate SELinux context.

1. Click *Save*.
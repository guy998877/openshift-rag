# Changing seLinuxChangePolicy at the namespace level

After applying the desired setting for `seLinuxChangePolicy` at the namespace level, all subsequently created pods in that namespace inherit the setting. However, if desired, you can override the inherited `seLinuxChangePolicy` setting for individual pods. Setting `seLinuxChangePolicy` at the pod level overrides inheritance from the namespace level setting for that pod.

.Prerequisites

- Logged in to a running OpenShift Container Platform cluster with administrator privileges.

- Access to the OpenShift Container Platform console.

.Procedure

To set `SELinuxChangePolicy` per namespace:

1. Select the desired namespace:

.. Click *Administration* > *Namespaces*. 

.. On the *Namespaces* page, click the desired namespace. The *Namespace details* page appears.

1. Add the `seLinuxChangePolicy` label to the namespace:

.. On the *Namespace details* page, next to *Labels*, click *Edit*.

.. In the *Edit labels* dialog, add the label `storage.openshift.io/selinux-change-policy=Recursive`.
This specifies recursively relabeling all files on pod volumes to the appropriate SELinux context.

.. Click *Save*.

.Verification
Start up a pod in the previously edited namespace and observe that the parameter `spec.securityContext.seLinuxChangePolicy` is set to `Recursive`.

.Example pod YAML file showing `seLinuxChangePolicy` setting
```yaml
securityContext:
    seLinuxOptions:
      level: 's0:c27,c19'
    runAsNonRoot: true
    fsGroup: 1000740000
    seccompProfile:
      type: RuntimeDefault
    seLinuxChangePolicy: Recursive <1>
  ...
```
<1> This value is inherited from the namespace.
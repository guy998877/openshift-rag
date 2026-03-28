# Changing fsGroup at the namespace level

After applying the desired setting for `fsGroupChangePolicy` at the namespace level, all subsequently created pods in that namespace inherit the setting. However, if desired, you can override the inherited `fsGroupChangePolicy` setting for individual pods. Setting `fsGroupChangePolicy` at the pod level overrides inheritance from the namespace level setting for that pod.

.Prerequisites

- Logged in to a running OpenShift Container Platform cluster with administrator privileges.

- Access to the OpenShift Container Platform console.

.Procedure

To set `fsGroupChangePolicy` per namespace:

1. Select the desired namespace:

.. Click *Administration* > *Namespaces*. 

.. On the *Namespaces* page, click the desired namespace. The *Namespace details* page appears.

1. Add the `fsGroupChangePolicy` label to the namespace:

.. On the *Namespace details* page, next to *Labels*, click *Edit*.

.. In the *Edit labels* dialog, add the label `storage.openshift.io/fsgroup-change-policy` and set it equal to either:
- `OnRootMismatch`: Specifies only changing permissions and ownership if the permission and the ownership of root directory does not match with expected permissions of the volume, thus helping to avoid pod timeout problems.
- `Always`: (Default) Specifies always changing permission and ownership of the volume when a volume is mounted.

.. Click *Save*.

.Verification
Start up a pod in the previously edited namespace and observe that the parameter `spec.securityContext.fsGroupChangePolicy` contains the value that you set for the namespace.

.Example pod YAML file showing `fsGroupChangePolicy` setting
```yaml
securityContext:
  seLinuxOptions:
    level: 's0:c27,c24'
  runAsNonRoot: true
  fsGroup: 1000750000
  fsGroupChangePolicy: OnRootMismatch <1>
  ...
```
<1> This value is inherited from the namespace.
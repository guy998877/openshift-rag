# Example PreflightValidationOCP resource

The following example shows a `PreflightValidationOCP` resource in the YAML format.

The example verifies all of the currently present modules against the upcoming `5.14.0-570.19.1.el9_6.x86_64` kernel. Because `.spec.pushBuiltImage` is set to `true`, KMM pushes the resulting images of Build/Sign into the defined repositories.

```yaml
apiVersion: kmm.sigs.x-k8s.io/v1beta2
kind: PreflightValidationOCP
metadata:
  name: preflight
spec:
  kernelVersion: 5.14.0-570.19.1.el9_6.x86_64
  dtkImage: quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:fe0322730440f1cbe6fffaaa8cac131b56574bec8abe3ec5b462e17557fecb32 
  pushBuiltImage: true
```
# Setting resource requests for a nodeAgent pod

Use the `configuration.nodeAgent.podConfig.resourceAllocations` specification field to set specific resource requests for a `nodeAgent` pod.

.Procedure

1. Set the `cpu` and `memory` resource requests in the YAML file:
```yaml
apiVersion: oadp.openshift.io/v1alpha1
kind: DataProtectionApplication
metadata:
  name: ts-dpa
spec:
  backupLocations:
  - velero:
      default: true
      objectStorage:
        bucket: oadp.....njph 
        prefix: velero
      credential:
        key: cloud
        name: cloud-credentials-gcp
      provider: gcp 
  configuration:
    velero:
      defaultPlugins:
      - gcp
      - openshift
      - csi
    nodeAgent:
      enable: true
      uploaderType: kopia
      podConfig:
        resourceAllocations:
          requests:
            cpu: 1000m
            memory: 16Gi
```
where:
`resourceAllocations`:: The resource allocation examples shown are for average usage.
`memory`:: You can modify this parameter depending on your infrastructure and usage.

1. Create the DPA CR by running the following command:
```bash
$ oc create -f nodeAgent.yaml
```

.Verification

1. Verify that the `nodeAgent` pods are running by using the following command:
```bash
$ oc get pods
```
.Example output
```bash
NAME                                                        READY   STATUS      RESTARTS   AGE
node-agent-hbj9l                                            1/1     Running     0          97s
node-agent-wmwgz                                            1/1     Running     0          95s
node-agent-zvc7k                                            1/1     Running     0          98s
openshift-adp-controller-manager-7f9db86d96-4lhgq           1/1     Running     0          137m
velero-7b6c7fb8d7-ppc8m                                     1/1     Running     0          4m2s
```

1. Check the resource requests by describing one of the `nodeAgent` pod:
```bash
$ oc describe pod node-agent-hbj9l | grep -C 5 Requests
```
.Example output
```bash
      --log-format=text
    State:          Running
      Started:      Mon, 09 Jun 2025 16:22:15 +0530
    Ready:          True
    Restart Count:  0
    Requests:
      cpu:     1
      memory:  1Gi
    Environment:
      NODE_NAME:            (v1:spec.nodeName)
      VELERO_NAMESPACE:    openshift-adp (v1:metadata.namespace)
```
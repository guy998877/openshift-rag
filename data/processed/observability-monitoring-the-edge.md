# Monitoring at the far edge network

OpenShift Container Platform clusters at the edge must keep the footprint of the platform components to a minimum. 
The following procedure is an example of how to configure a single-node OpenShift or a node at the far edge network with a small monitoring footprint.

.Prerequisites

- For environments that use Red Hat Advanced Cluster Management (RHACM), you have enabled the Observability service. 
- The hub cluster is running Red Hat OpenShift Data Foundation (ODF).

.Procedure

1. Create a `ConfigMap` CR, and save it as `monitoringConfigMap.yaml`, as in the following example: 
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
 name: cluster-monitoring-config
 namespace: openshift-monitoring
 data:
 config.yaml: |
   alertmanagerMain:
     enabled: false
   telemeterClient:
     enabled: false
   prometheusK8s:
      retention: 24h
```

1. Apply the `ConfigMap` CR by running the following command on the single-node OpenShift cluster:
```bash
$ oc apply -f monitoringConfigMap.yaml
```

1. Create a `Namespace` CR, and save it as `monitoringNamespace.yaml`, as in the following example:
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: open-cluster-management-observability
```

1. Apply the `Namespace` CR by running the following command on the hub cluster :
```bash
$ oc apply -f monitoringNamespace.yaml
```

1. Create an `ObjectBucketClaim` CR, and save it as `monitoringObjectBucketClaim.yaml`, as in the following example:
```yaml
apiVersion: objectbucket.io/v1alpha1
kind: ObjectBucketClaim
metadata:
  name: multi-cloud-observability
  namespace: open-cluster-management-observability
spec:
  storageClassName: openshift-storage.noobaa.io
  generateBucketName: acm-multi
```

1. Apply the `ObjectBucketClaim` CR by running the following command on the hub cluster:
```bash
$ oc apply -f monitoringObjectBucketClaim.yaml
```

1. Create a `Secret` CR, and save it as `monitoringSecret.yaml`, as in the following example:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: multiclusterhub-operator-pull-secret
  namespace: open-cluster-management-observability
stringData:
  .dockerconfigjson: 'PULL_SECRET'
```

1. Apply the `Secret` CR by running the following command in the hub cluster:
```bash
$ oc apply -f monitoringSecret.yaml
```

1. Get the keys for the NooBaa service and the back-end bucket name from the hub cluster by running the following commands:
```bash
$ NOOBAA_ACCESS_KEY=$(oc get secret noobaa-admin -n openshift-storage -o json | jq -r '.data.AWS_ACCESS_KEY_ID|@base64d')
```
```bash
$ NOOBAA_SECRET_KEY=$(oc get secret noobaa-admin -n openshift-storage -o json | jq -r '.data.AWS_SECRET_ACCESS_KEY|@base64d')
```
```bash
$ OBJECT_BUCKET=$(oc get objectbucketclaim -n open-cluster-management-observability multi-cloud-observability -o json | jq -r .spec.bucketName)
```

1. Create a `Secret` CR for bucket storage and save it as `monitoringBucketSecret.yaml`, as in the following example:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: thanos-object-storage
  namespace: open-cluster-management-observability
type: Opaque
stringData:
  thanos.yaml: |
    type: s3
    config:
      bucket: ${OBJECT_BUCKET}
      endpoint: s3.openshift-storage.svc
      insecure: true
      access_key: ${NOOBAA_ACCESS_KEY}
      secret_key: ${NOOBAA_SECRET_KEY}
```

1. Apply the `Secret` CR by running the following command on the hub cluster:
```bash
$ oc apply -f monitoringBucketSecret.yaml
```

1. Create the `MultiClusterObservability` CR and save it as `monitoringMultiClusterObservability.yaml`, as in the following example:
```yaml
---- 
apiVersion: observability.open-cluster-management.io/v1beta2
kind: MultiClusterObservability
metadata:
  name: observability
spec:
  advanced:
    retentionConfig:
      blockDuration: 2h
      deleteDelay: 48h
      retentionInLocal: 24h
      retentionResolutionRaw: 3d
  enableDownsampling: false
  observabilityAddonSpec:
    enableMetrics: true
    interval: 300
  storageConfig:
    alertmanagerStorageSize: 10Gi
    compactStorageSize: 100Gi
    metricObjectStorage:
      key: thanos.yaml
      name: thanos-object-storage
    receiveStorageSize: 25Gi
    ruleStorageSize: 10Gi
    storeStorageSize: 25Gi
```

1. Apply the `MultiClusterObservability` CR by running the following command on the hub cluster:
```bash
$ oc apply -f monitoringMultiClusterObservability.yaml
```

.Verification

1. Check the routes and pods in the namespace to validate that the services have deployed on the hub cluster by running the following command:
```bash
$ oc get routes,pods -n open-cluster-management-observability
```
.Example output
```bash
NAME                                         HOST/PORT                                                                                        PATH      SERVICES                          PORT          TERMINATION          WILDCARD
route.route.openshift.io/alertmanager        alertmanager-open-cluster-management-observability.cloud.example.com        /api/v2   alertmanager                      oauth-proxy   reencrypt/Redirect   None
route.route.openshift.io/grafana             grafana-open-cluster-management-observability.cloud.example.com                       grafana                           oauth-proxy   reencrypt/Redirect   None <1>
route.route.openshift.io/observatorium-api   observatorium-api-open-cluster-management-observability.cloud.example.com             observability-observatorium-api   public        passthrough/None     None
route.route.openshift.io/rbac-query-proxy    rbac-query-proxy-open-cluster-management-observability.cloud.example.com              rbac-query-proxy                  https         reencrypt/Redirect   None

NAME                                                           READY   STATUS    RESTARTS   AGE
pod/observability-alertmanager-0                               3/3     Running   0          1d
pod/observability-alertmanager-1                               3/3     Running   0          1d
pod/observability-alertmanager-2                               3/3     Running   0          1d
pod/observability-grafana-685b47bb47-dq4cw                     3/3     Running   0          1d
<...snip…>
pod/observability-thanos-store-shard-0-0                       1/1     Running   0          1d
pod/observability-thanos-store-shard-1-0                       1/1     Running   0          1d
pod/observability-thanos-store-shard-2-0                       1/1     Running   0          1d

```
<1> A dashboard is accessible at the grafana route listed. You can use this to view metrics across all managed clusters.

For more information on observability in Red Hat Advanced Cluster Management, see [Observability](https://docs.redhat.com/en/documentation/red_hat_advanced_cluster_management_for_kubernetes/2.12/html/observability/index).
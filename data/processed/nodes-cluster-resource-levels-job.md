# Running the OpenShift Cluster Capacity Tool as a job inside a pod

You can run the OpenShift Cluster Capacity Tool as a job inside of a pod by using a `ConfigMap` object. This allows you to run the tool multiple times without needing user intervention.

.Prerequisites

- Download and install the OpenShift Cluster Capacity Tool from the `cluster-capacity` repository. See the link in the "Additional resources" section.

.Procedure

1. Create the cluster role:

.. Create a YAML file similar to the following:
```yaml
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: cluster-capacity-role
rules:
- apiGroups: [""]
  resources: ["pods", "nodes", "persistentvolumeclaims", "persistentvolumes", "services", "replicationcontrollers"]
  verbs: ["get", "watch", "list"]
- apiGroups: ["apps"]
  resources: ["replicasets", "statefulsets"]
  verbs: ["get", "watch", "list"]
- apiGroups: ["policy"]
  resources: ["poddisruptionbudgets"]
  verbs: ["get", "watch", "list"]
- apiGroups: ["storage.k8s.io"]
  resources: ["storageclasses"]
  verbs: ["get", "watch", "list"]
```

.. Create the cluster role by running the following command:
```bash
$ oc create -f <file_name>.yaml
```
For example:
```bash
$ oc create sa cluster-capacity-sa
```

1. Create the service account:
```bash
$ oc create sa cluster-capacity-sa -n default
```

1. Add the role to the service account:
```bash
$ oc adm policy add-cluster-role-to-user cluster-capacity-role \
    system:serviceaccount:<namespace>:cluster-capacity-sa
```
where:

<namespace>:: Specifies the namespace where the pod is located.

1. Define and create the pod spec:

.. Create a YAML file similar to the following:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: small-pod
  labels:
    app: guestbook
    tier: frontend
spec:
  securityContext:
    runAsNonRoot: true
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: php-redis
    image: gcr.io/google-samples/gb-frontend:v4
    imagePullPolicy: Always
    resources:
      limits:
        cpu: 150m
        memory: 100Mi
      requests:
        cpu: 150m
        memory: 100Mi
    securityContext:
      allowPrivilegeEscalation: false
      capabilities:
        drop: [ALL]
```

.. Create the pod by running the following command:
```bash
$ oc create -f <file_name>.yaml
```
For example:
```bash
$ oc create -f pod.yaml
```

1. Created a config map object by running the following command:
```bash
$ oc create configmap cluster-capacity-configmap \
    --from-file=pod.yaml=pod.yaml
```
The cluster capacity analysis is mounted in a volume using a config map object named `cluster-capacity-configmap` to mount the input pod spec file `pod.yaml` into a volume `test-volume` at the path `/test-pod`.

1. Create the job using the below example of a job specification file:

.. Create a YAML file similar to the following:
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: cluster-capacity-job
spec:
  parallelism: 1
  completions: 1
  template:
    metadata:
      name: cluster-capacity-pod
    spec:
        containers:
        - name: cluster-capacity
          image: openshift/origin-cluster-capacity
          imagePullPolicy: "Always"
          volumeMounts:
          - mountPath: /test-pod
            name: test-volume
          env:
          - name: CC_INCLUSTER
            value: "true"
          command:
          - "/bin/sh"
          - "-ec"
          - |
            /bin/cluster-capacity --podspec=/test-pod/pod.yaml --verbose
        restartPolicy: "Never"
        serviceAccountName: cluster-capacity-sa
        volumes:
        - name: test-volume
          configMap:
            name: cluster-capacity-configmap
```
where:

`spec.template.spec.containers.env`:: Specifies a required environment variable that indicates the Cluster Capacity Tool is running inside a cluster as a pod.
The `pod.yaml` key of the `ConfigMap` object is the same as the `Pod` spec file name, though it is not required. By doing this, the input pod spec file can be accessed inside the pod as `/test-pod/pod.yaml`.

.. Run the cluster capacity image as a job in a pod by running the following command:
```bash
$ oc create -f cluster-capacity-job.yaml
```

.Verification

1. Check the job logs to find the number of pods that can be scheduled in the cluster:
```bash
$ oc logs jobs/cluster-capacity-job
```
.Example output
```bash
small-pod pod requirements:
        - CPU: 150m
        - Memory: 100Mi

The cluster can schedule 52 instance(s) of the pod small-pod.

Termination reason: Unschedulable: No nodes are available that match all of the
following predicates:: Insufficient cpu (2).

Pod distribution among nodes:
small-pod
        - 192.168.124.214: 26 instance(s)
        - 192.168.124.120: 26 instance(s)
```
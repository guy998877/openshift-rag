# Creating CRDs for volume populators

The following procedure explains how to create an example "hello, world" custom resource definition (CRD) for a volume populator.

Users can then create instances of this CRD to populate persistent volume claims (PVCs).

.Prerequisites

- Access to the OpenShift Container Platform web console.

- Access to the cluster with cluster-admin privileges.

.Procedure

1. Create a namespace for the logical grouping and operation of the populator, and related resources, using the following example YAML file:
.Example namespace YAML file
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: hello
```

1. Create a CRD for your data source using the following example YAML file:
.Example CRD YAML file
```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: hellos.hello.example.com
spec:
  group: hello.example.com
  names:
    kind: Hello
    listKind: HelloList
    plural: hellos
    singular: hello
  scope: Namespaced
  versions:
  - name: v1alpha1
    schema:
      openAPIV3Schema:
        description: Hello is a specification for a Hello resource
        properties:
          apiVersion:
            description: 'APIVersion defines the versioned schema of this representation
              of an object. Servers should convert recognized schemas to the latest
              internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources'
            type: string
          kind:
            description: 'Kind is a string value representing the REST resource this
              object represents. Servers may infer this from the endpoint the client
              submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds'
            type: string
          spec:
            description: HelloSpec is the spec for a Hello resource
            properties:
              fileContents:
                type: string
              fileName:
                type: string
            required:
            - fileContents
            - fileName
            type: object
        required:
        - spec
        type: object
    served: true
    storage: true
```

1. Deploy the controller by creating a `ServiceAccount`, `ClusterRole`, `ClusterRoleBindering`, and `Deployment` to run the logic that implements the population:

.. Create a service account for the populator using the following example YAML file:
.Example service account YAML file
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: hello-account
  namespace: hello <1>
```
<1> Reference the namespace that you created earlier.

.. Create a cluster role for the populator using the following example YAML file:
.Example cluster role YAML file
```yaml
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: hello-role
rules:
  - apiGroups: [hello.example.com]
    resources: [hellos]
    verbs: [get, list, watch]
```

.. Create a cluster role binding using the following example YAML file:
.Example cluster role binding YAML file
```yaml
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: hello-binding <1>
subjects:
  - kind: ServiceAccount
    name: hello-account <2>
    namespace: hello <3>
roleRef:
  kind: ClusterRole
  name: hello-role <4>
  apiGroup: rbac.authorization.k8s.io
```
<1> Role binding name.
<2> Reference the name of the service account that you created earlier.
<3> Reference the name of the namespace for the service account that you created earlier.
<4> Reference the cluster role you created earlier.

.. Create a Deployment for the populator using the following example YAML file:
.Example deployment YAML file
```yaml
kind: Deployment
apiVersion: apps/v1
metadata:
  name: hello-populator
  namespace: hello <1>
spec:
  selector:
    matchLabels:
      app: hello
  template:
    metadata:
      labels:
        app: hello
    spec:
      serviceAccount: hello-account <2>
      containers:
        - name: hello
          image: registry.k8s.io/sig-storage/hello-populator:v1.0.1
          imagePullPolicy: IfNotPresent
          args:
            - --mode=controller
            - --image-name=registry.k8s.io/sig-storage/hello-populator:v1.0.1
            - --http-endpoint=:8080
          ports:
            - containerPort: 8080
              name: http-endpoint
              protocol: TCP
```
<1> Reference the namespace that you created earlier.
<2> Reference the service account that you created earlier.

1. Create a volume populator to register the `kind:Hello` resource as a valid data source for the volume using the following example YAML file:
.Example volume populator YAML file
```yaml
kind: VolumePopulator
apiVersion: populator.storage.k8s.io/v1beta1
metadata:
  name: hello-populator <1>
sourceKind:
  group: hello.example.com
  kind: Hello
```
<1> Volume populator name.
PVCs that use an unregistered populator generate an event: "The datasource for this PVC does not match any registered VolumePopulator", indicating that the PVC might not be provisioned because you are using an unknown (unregistered) populator. 

.Next steps
- You can now create CR instances of this CRD to populate PVCs.
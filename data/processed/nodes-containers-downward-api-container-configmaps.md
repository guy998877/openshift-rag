# Consuming configuration maps using the Downward API

When creating pods, you can use the Downward API to inject configuration map values
so that image and application authors can create an image for specific environments.

.Procedure

1. Create a config map with the values to inject:

.. Create a `*_configmap.yaml_*` file similar to the following:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: myconfigmap
data:
  mykey: myvalue
```

.. Create the config map from the `configmap.yaml` file by using the following command:
```bash
$ oc create -f configmap.yaml
```

1. Create a pod that references the above config map:

.. Create a `pod.yaml` file similar to the following:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: dapi-env-test-pod
spec:
  securityContext:
    runAsNonRoot: true
    seccompProfile:
      type: RuntimeDefault
  containers:
    - name: env-test-container
      image: gcr.io/google_containers/busybox
      command: [ "/bin/sh", "-c", "env" ]
      env:
        - name: MY_CONFIGMAP_VALUE
          valueFrom:
            configMapKeyRef:
              name: myconfigmap
              key: mykey
      securityContext:
        allowPrivilegeEscalation: false
        capabilities:
          drop: [ALL]
  restartPolicy: Always
# ...
```

.. Create the pod from the `pod.yaml` file by using the following command:
```bash
$ oc create -f pod.yaml
```

.Verification

- Check the container's logs for the `MY_CONFIGMAP_VALUE` value by using the following command:
```bash
$ oc logs -p dapi-env-test-pod
```
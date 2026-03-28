# Configuring /dev/fuse for unprivileged builds in pods

You can grant an unprivileged pod the capability to perform Filesystem in Userspace (FUSE) mounts by exposing the `/dev/fuse` device. With this setup, an unprivileged user within the pod can use tools such as `podman` with storage drivers such as `fuse-overlayfs` by mimicking privileged build capabilities in a secure and efficient manner without granting full privileged access to the pod.

You expose the `/dev/fuse` device by adding the `io.kubernetes.cri-o.Devices: "/dev/fuse"` annotation to your pod definition.

.Procedure

1. Define the pod with `/dev/fuse` access:
.. Create a YAML file named `fuse-builder-pod.yaml` with the following content: 
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: fuse-builder-pod
  annotations:
    io.kubernetes.cri-o.Devices: "/dev/fuse"
spec:
  containers:
  - name: build-container
    image: quay.io/podman/stable
    command: ["/bin/sh", "-c"]
    args: ["echo 'Container is running. Use oc exec to get a shell.'; sleep infinity"]
    securityContext:
      runAsUser: 1000
```
where:
`metadata.annotations`:: Specifies that the `io.kubernetes.cri-o.Devices: "/dev/fuse"` annotation makes the FUSE device available.
`spec.containers.image`:: Specifies a container that uses an image that includes `podman` (for example, `quay.io/podman/stable`).
`spec.containers.args`:: Specifies a command to keep the container running so you can `exec` into it.
`spec.containers.securityContext`:: Specifies a `securityContext` that runs the container as an unprivileged user (for example, `runAsUser: 1000`).
> **NOTE:** Depending on your cluster's Security Context Constraints (SCCs) or other policies, you might need to further adjust the `securityContext` specification, for example, by allowing specific capabilities if `/dev/fuse` alone is not sufficient for `fuse-overlayfs` to operate.
.. Create the pod by running the following command:
```bash
$ oc apply -f fuse-builder-pod.yaml
```

1. Verify that the pod is running by running the following command:
```bash
$ oc get pods fuse-builder-pod
```

1. Access the pod and prepare the build environment:

.. After the `fuse-builder-pod` pod is in the `Running` state, open a shell session into the `build-container` environment by running the following command:
```bash
$ oc exec -ti fuse-builder-pod -- /bin/bash
```
You are now inside the container. 

.. Because the default working directory might not be writable by an unprivileged user, change to a writable directory such as `/tmp` by running the following commands:
```bash
$ cd /tmp
```
```bash
$ pwd
```
```bash
/tmp
```

1. Create a dockerfile and build an image by using Podman:
Inside the pod's shell and within the `/tmp` directory, you can now create a `Dockerfile` and use `podman` to build a container image. If `fuse-overlayfs` is the default or configured storage driver, Podman is able to leverage `fuse-overlayfs` because of the available `/dev/fuse` device.
.. Create a sample `Dockerfile`:
```bash
$ cat > Dockerfile <<EOF
FROM registry.access.redhat.com/ubi9/ubi-minimal
RUN microdnf install -y findutils && microdnf clean all
RUN echo "This image was built inside a pod with /dev/fuse by user $(id -u)" > /app/build_info.txt
COPY Dockerfile /app/Dockerfile_copied
WORKDIR /app
CMD ["sh", "-c", "cat /app/build_info.txt && echo '--- Copied Dockerfile ---' && cat /app/Dockerfile_copied"]
EOF
```
.. Build the image by running the following command. The `-t` flag tags the image.
```bash
$ podman build -t my-fuse-built-image:latest .
```
You should see Podman executing the build steps.

1. Optional: Test the built image:
Still inside the `fuse-builder-pod`, you can run a container from the image you just built to test it by running the following command:
```bash
$ podman run --rm my-fuse-built-image:latest
```
This should output the content of the `/app/build_info.txt` file and the copied Dockerfile.

1. Exit the pod and clean up:
.. After you are done, exit the shell session in the pod by running the following command:
```bash
$ exit
```
.. Delete the pod if it is no longer needed by running the following command:
```bash
$ oc delete pod fuse-builder-pod
```
.. Remove the local YAML file by running the following command:
```bash
$ rm fuse-builder-pod.yaml
```
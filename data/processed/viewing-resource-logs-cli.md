# Viewing resource logs by using the CLI

Use the following procedure to view resource logs by using the command-line interface (CLI).

.Prerequisites

- Access to the pass:quotes[OpenShift CLI (`oc`)].

.Procedure

- View the log for a specific pod by entering the following command:
```bash
$ oc logs -f <pod_name> -c <container_name>
```
--
where:

`-f`:: Optional: Specifies that the output follows what is being written into the logs.
`<pod_name>`:: Specifies the name of the pod.
`<container_name>`:: Optional: Specifies the name of a container. When a pod has more than one container, you must specify the container name.
--
For example:
```bash
$ oc logs -f ruby-57f7f4855b-znl92 -c ruby
```

- View the log for a specific resource by entering the following command:
```bash
$ oc logs <object_type>/<resource_name>
```
For example:
```bash
$ oc logs deployment/ruby
```
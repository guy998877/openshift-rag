# Executing remote commands in containers

You can use the OpenShift CLI (`oc`) to execute remote commands in OpenShift Container Platform containers. By running commands in a container, you can perform troubleshooting, inspect logs, run scripts, and other tasks.

.Procedure

- Use a command similar to the following to run a command in a container:
```bash
$ oc exec <pod> [-c <container>] -- <command> [<arg_1> ... <arg_n>]
```
For example:
```bash
$ oc exec mypod date
```
.Example output
```bash
Thu Apr  9 02:21:53 UTC 2015
```
> **IMPORTANT:** link:https://access.redhat.com/errata/RHSA-2015:1650[For security purposes], the `oc exec` command does not work when accessing privileged containers except when the command is executed by a `cluster-admin` user.
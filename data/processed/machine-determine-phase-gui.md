# Determining the phase of a machine by using the web console

You can find the phase of a machine by using the OpenShift Container Platform web console.

.Prerequisites

- You have access to an OpenShift Container Platform cluster using an account with `cluster-admin` permissions.

.Procedure

1. Log in to the web console as a user with the `cluster-admin` role.

1. Navigate to *Compute* -> *Machines*.

1. On the *Machines* page, select the name of the machine that you want to find the phase of.

1. On the *Machine details* page, select the *YAML* tab.

1. In the YAML block, find the value of the `status.phase` field.
.Example YAML snippet
```yaml
apiVersion: machine.openshift.io/v1beta1
kind: Machine
metadata:
  name: mycluster-5kbsp-worker-us-west-1a-fmx8t
# ...
status:
  phase: Running # <1>
```
<1> In this example, the phase is `Running`.
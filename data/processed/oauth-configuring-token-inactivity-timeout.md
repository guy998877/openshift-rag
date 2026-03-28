# Configuring token inactivity timeout for the internal OAuth server

You can configure OAuth tokens to expire after a set period of inactivity. By default, no token inactivity timeout is set.

> **NOTE:** If the token inactivity timeout is also configured in your OAuth client, that value overrides the timeout that is set in the internal OAuth server configuration.

.Prerequisites

- You have access to the cluster as a user with the `cluster-admin` role.
- You have configured an identity provider (IDP).

.Procedure

1. Update the `OAuth` configuration to set a token inactivity timeout.

.. Edit the `OAuth` object:
```bash
$ oc edit oauth cluster
```
Add the `spec.tokenConfig.accessTokenInactivityTimeout` field and set your timeout value:
```yaml
apiVersion: config.openshift.io/v1
kind: OAuth
metadata:
...
spec:
  tokenConfig:
    accessTokenInactivityTimeout: 400s <1>
```
<1> Set a value with the appropriate units, for example `400s` for 400 seconds, or `30m` for 30 minutes. The minimum allowed timeout value is `300s`.

.. Save the file to apply the changes.

1. Check that the OAuth server pods have restarted:
```bash
$ oc get clusteroperators authentication
```
Do not continue to the next step until `PROGRESSING` is listed as `False`, as shown in the following output:
.Example output
```bash
NAME             VERSION   AVAILABLE   PROGRESSING   DEGRADED   SINCE
authentication   4.21.0    True        False         False      145m
```

1. Check that a new revision of the Kubernetes API server pods has rolled out. This will take several minutes.
```bash
$ oc get clusteroperators kube-apiserver
```
Do not continue to the next step until `PROGRESSING` is listed as `False`, as shown in the following output:
.Example output
```bash
NAME             VERSION   AVAILABLE   PROGRESSING   DEGRADED   SINCE
kube-apiserver   4.21.0     True        False         False      145m
```
If `PROGRESSING` is showing `True`, wait a few minutes and try again.

.Verification

1. Log in to the cluster with an identity from your IDP.

1. Execute a command and verify that it was successful.

1. Wait longer than the configured timeout without using the identity. In this procedure's example, wait longer than 400 seconds.

1. Try to execute a command from the same identity's session.
This command should fail because the token should have expired due to inactivity longer than the configured timeout.
.Example output
```bash
error: You must be logged in to the server (Unauthorized)
```
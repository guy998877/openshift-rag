# Configuring the internal OAuth server's token duration

You can configure default options for the internal OAuth server's
token duration.

> **IMPORTANT:** By default, tokens are only valid for 24 hours. Existing sessions expire after this time elapses.

If the default time is insufficient, then this can be modified using
the following procedure.

.Procedure

1. Create a configuration file that contains the token duration options. The
following file sets this to 48 hours, twice the default.
```yaml
apiVersion: config.openshift.io/v1
kind: OAuth
metadata:
  name: cluster
spec:
  tokenConfig:
    accessTokenMaxAgeSeconds: 172800 <1>
```
<1> Set `accessTokenMaxAgeSeconds` to control the lifetime of access tokens.
The default lifetime is 24 hours, or 86400 seconds. This attribute cannot
be negative. If set to zero, the default lifetime is used.

1. Apply the new configuration file:
> **NOTE:** Because you update the existing OAuth server, you must use the `oc apply` command to apply the change.
```bash
$ oc apply -f </path/to/file.yaml>
```

1. Confirm that the changes are in effect:
```bash
$ oc describe oauth.config.openshift.io/cluster
```
.Example output
```bash
...
Spec:
  Token Config:
    Access Token Max Age Seconds:  172800
...
```
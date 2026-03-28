# Changing CVO log level (Technology Preview)

:FeatureName: Changing the CVO log level

The Cluster Version Operator (CVO) log level verbosity can be changed by the cluster administrator. There are four log levels.

- `Normal` - The default log level. Contains working log information. Used when everything is fine. Provides helpful notices for auditing or common operations.
- `Debug` - Used when something goes wrong. Expect a higher quantity of notices.
- `Trace` - Used to diagnose errors.
- `TraceAll` - Used to get the complete body content of the logs.

> **NOTE:** If `TraceAll` is turned on in a production cluster it may cause widespread performance issues and large log files.

.Prerequisites
- You have access to the cluster as a user with the `cluster-admin` role.
- You have installed the pass:quotes[OpenShift CLI (`oc`)].
- You have the `TechPreviewNoUpgrade` feature set enabled.

.Procedure

1. Enter the following command into the CLI to change the log level.

```bash
$ oc patch clusterversionoperator/cluster --type=merge --patch '{"spec":{"operatorLogLevel":"<log_level>"}}'
```

.Example output
```bash
clusterversionoperator.operator.openshift.io/cluster patched
```
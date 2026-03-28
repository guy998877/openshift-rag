# Specifying OpenShift Container Platform installer log levels

By default, the OpenShift Container Platform installer log level is set to `info`. If more detailed logging is required when diagnosing a failed OpenShift Container Platform installation, you can increase the `openshift-install` log level to `debug` when starting the installation again.

.Prerequisites

- You have access to the installation host.

.Procedure

- Set the installation log level to `debug` when initiating the installation:
```bash
$ ./openshift-install --dir <installation_directory> wait-for bootstrap-complete --log-level debug
```
where::
- Possible log levels include `info`, `warn`, `error,` and `debug`.
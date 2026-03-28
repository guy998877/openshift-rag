# Update recommendations in the channel

OpenShift Container Platform maintains an update recommendation service that knows your installed OpenShift Container Platform version and the path to take within the channel to get you to the next release.

Update paths are also limited to versions relevant to your currently selected channel and its promotion characteristics.

You can imagine seeing the following releases in your channel:

- 4.21.0
- 4.21.1
- 4.21.3
- 4.21.4

The service recommends only updates that have been tested and have no known serious regressions. For example, if your cluster is on 4.21.1 and OpenShift Container Platform suggests 4.21.4, then it is recommended to update from 4.21.1 to 4.21.4.

> **IMPORTANT:** Do not rely on consecutive patch numbers. In this example, 4.21.2 is not and never was available in the channel, therefore updates to 4.21.2 are not recommended or supported.
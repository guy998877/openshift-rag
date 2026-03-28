# Starting the cluster update

When updating from one y-stream release to the next, you must ensure that the intermediate z-stream releases are also compatible.

> **NOTE:** You can verify that you are updating to a viable release by running the `oc adm upgrade` command. The `oc adm upgrade` command lists the compatible update releases.

.Procedure

1. Start the update:
--
```bash
$ oc adm upgrade --to=4.15.33
```

> **IMPORTANT:** * **Control plane only update**: Ensure you point to the interim <y+1> release path * **Y-stream update** - Ensure you use the correct <y.z> release that follows the Kubernetes link:https://kubernetes.io/releases/version-skew-policy/[version skew policy]. * **Z-stream update** - Verify that there are no problems moving to that specific release

.Example output
```bash
Requested update to 4.15.33 <1>
```
<1> The `Requested update` value changes depending on your particular update.
--
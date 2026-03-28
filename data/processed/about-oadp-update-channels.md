# About OADP update channels

When you install an OADP Operator, you choose an update channel. This channel determines which upgrades to the OADP Operator and to Velero you receive.

The following update channels are available:

- The *stable-1.3* channel contains `OADP.v1.3.z`, the most recent OADP 1.3 `ClusterServiceVersion`.

- The *stable-1.4* channel contains `OADP.v1.4.z`, the most recent OADP 1.4 `ClusterServiceVersion`.

- Starting with OADP 1.5 on OpenShift Container Platform v4.19, OADP reintroduces the *stable* channel which contains a single supported OADP version for a particular OpenShift Container Platform version.

For more information, see [OpenShift Operator Life Cycles](https://access.redhat.com/support/policy/updates/openshift_operators).

*Which update channel is right for you?*

- If you are already using the *stable* channel, you will continue to get updates from `OADP.v1.5.z`.

- Choose the *stable-1.y* update channel to install OADP 1.y and to continue receiving patches for it. If you choose this channel, you will receive all z-stream patches for version 1.y.z.

*When must you switch update channels?*

- If you have OADP 1.y installed, and you want to receive patches only for that y-stream, you must switch from the *stable* update channel to the *stable-1.y* update channel. You will then receive all z-stream patches for version 1.y.z.

- If you have OADP 1.0 installed, want to upgrade to OADP 1.1, and then receive patches only for OADP 1.1, you must switch from the *stable-1.0* update channel to the *stable-1.1* update channel. You will then receive all z-stream patches for version 1.1.z.

- If you have OADP 1.y installed, with _y_ greater than 0, and want to switch to OADP 1.0, you must uninstall your OADP Operator and then reinstall it using the *stable-1.0* update channel. You will then receive all z-stream patches for version 1.0.z.

> **NOTE:** You cannot switch from OADP 1.y to OADP 1.0 by switching update channels. You must uninstall the Operator and then reinstall it.
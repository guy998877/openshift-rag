# Control Plane Only updates for layered products and Operators installed through Operator Lifecycle Manager

In addition to the Control Plane Only update steps mentioned for the web console and CLI, there are additional steps to consider when performing Control Plane Only updates for clusters with the following:

- Layered products
- Operators installed through Operator Lifecycle Manager (OLM)

.What is a layered product?

Layered products refer to products that are made of multiple underlying products that are intended to be used together and cannot be broken into individual subscriptions. For examples of layered OpenShift Container Platform products, see [Layered Offering On OpenShift](https://access.redhat.com/support/policy/updates/openshift/#layered).

As you perform a Control Plane Only update for the clusters of layered products and those of Operators that have been installed through OLM, you must complete the following:

1. You have updated all Operators previously installed through Operator Lifecycle Manager (OLM) to a version that is compatible with your target release. Updating the Operators ensures they have a valid update path when the default software catalogs switch from the current minor version to the next during a cluster update. See "Updating installed Operators" in the "Additional resources" section for more information on how to check compatibility and, if necessary, update the installed Operators.

1. Confirm the cluster version compatibility between the current and intended Operator versions. You can verify which versions your OLM Operators are compatible with by using the link:https://access.redhat.com/labs/ocpouic/?operator=logging&&ocp_versions=4.10,4.11,4.12[Red Hat OpenShift Container Platform Operator Update Information Checker].

As an example, here are the steps to perform a Control Plane Only update from <4.y> to <4.y+2> for 'OpenShift Data Foundation'. This can be done through the CLI or web console. For information about how to update clusters through your desired interface, see _Control Plane Only update using the web console_ and "Control Plane Only update using the CLI" in "Additional resources".

.Example workflow
1. Pause the worker machine pools.
1. Update OpenShift <4.y> -> OpenShift <4.y+1>.
1. Update ODF <4.y> -> ODF <4.y+1>.
1. Update OpenShift <4.y+1> -> OpenShift <4.y+2>.
1. Update to ODF <4.y+2>.
1. Unpause the worker machine pools.

> **NOTE:** The update to ODF <4.y+2> can happen before or after worker machine pools have been unpaused.
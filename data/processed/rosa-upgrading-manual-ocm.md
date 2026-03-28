//  adding this ifeval hcp-in-rosa when a hcp procedure appears in the rosa distro as well as the  hcp distro

# Upgrading with the OpenShift Cluster Manager console

You can schedule upgrades for a OpenShift Container Platform cluster manually either one time or on a recurring schedule by using OpenShift Cluster Manager console.

.Procedure

1. Log in to link:https://console.redhat.com/openshift[OpenShift Cluster Manager].
1. Select a cluster to upgrade.
1. Click the *Settings* tab.
1. In the *Update strategy* pane, select which type of update you want:
- For individual updates, you can request the upgrade either immediately (to start within an hour) or at a future time.
- For recurring updates, select a recurring date and time to start the upgrade automatically to the latest x.y.Z (z-stream) version available.
> **IMPORTANT:** Recurring updates are applicable only for z-stream updates. Minor version or y-stream updates need to be done manually. You will be notified when a new y-stream update is available.
1. In the *Update strategy* pane, click *Save* to apply your update strategy.
1. In the *Update status* pane, review the *Update available* information and click *Update*.
> **NOTE:** The *Update* button is enabled only when an upgrade is available.
1. The *Update cluster* dialog opens. Recommended cluster upgrades appear in the *Select version* pane. Select the version you want to upgrade your cluster to, and click *Next*.
1. Optional: For OpenShift Container Platform clusters that use AWS Security Token Service (STS), the account-level and cluster-specific Operator roles might need to be updated, depending on the selected target version.
.. In the ROSA CLI, run the `rosa list account-roles` command to list and verify that the account roles are compatible with the target minor version chosen for the upgrade. If the roles are not compatible, run the `rosa upgrade account-roles` command to upgrade the account roles to the latest OpenShift version.
.. In the ROSA CLI, run the `rosa list operator-roles` command to list and verify that Operator roles associated with the cluster are compatible with the target minor version chosen for the upgrade. If not, run the `rosa upgrade operators-roles` command to upgrade the cluster's Operator roles to the latest OpenShift version.
.. If you select an update version that requires approval, provide an administrator's acknowledgment by typing *Acknowledge* into the field provided, and click *Next*.
1. In the *Schedule update* dialog, schedule your cluster upgrade.
- To upgrade within an hour, select *Update now* and click *Next*.
- To upgrade at a later time, select *Schedule a different time* and set a time and date for your upgrade. Click *Next* to proceed to the confirmation dialog.
1. After reviewing the version and schedule summary, select *Confirm update*.
1. Click *Close* to exit out of the *Update cluster* dialog.

The cluster is scheduled for an upgrade to the target version. This action can take up to an hour, depending on the selected upgrade schedule and your workload configuration, such as pod disruption budgets.

The status is displayed in the *Update status* pane.

.Troubleshooting
- Sometimes a scheduled upgrade does not trigger. See link:https://access.redhat.com/solutions/6648291[Upgrade maintenance cancelled] for more information.
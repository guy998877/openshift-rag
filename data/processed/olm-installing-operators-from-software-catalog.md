# About Operator installation from the software catalog

The software catalog is a user interface for discovering Operators; it works in conjunction with Operator Lifecycle Manager (OLM), which installs and manages Operators on a cluster.

During installation, you must determine the following initial settings for the Operator:

Update Channel:: If an Operator is available through multiple channels, you can choose which channel you want to subscribe to. For example, to deploy from the *stable* channel, if available, select it from the list.

Approval Strategy:: You can choose automatic or manual updates.
If you choose automatic updates for an installed Operator, when a new version of that Operator is available in the selected channel, Operator Lifecycle Manager (OLM) automatically upgrades the running instance of your Operator without human intervention.
If you select manual updates, when a newer version of an Operator is available, OLM creates an update request. As a
cluster administrator,
you must then manually approve that update request to have the Operator updated to the new version.
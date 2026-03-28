# Starting a rolling deployment using the Developer perspective

You can upgrade an application by starting a rolling deployment.

.Prerequisites

- You are in the *Developer* perspective of the web console.
- You have created an application.

.Procedure

1. In the *Topology* view, click the application node to see the *Overview* tab in the side panel. Note that the *Update Strategy* is set to the default *Rolling* strategy.
1. In the *Actions* drop-down menu, select *Start Rollout* to start a rolling update. The rolling deployment spins up the new version of the application and then terminates the old one.
.Rolling update
image::odc-rolling-update.png[]
# Changing the update channel for an Operator

You can change the update channel for an Operator by using the OpenShift Container Platform web console.

> **TIP:** If the approval strategy in the subscription is set to *Automatic*, the update process initiates as soon as a new Operator version is available in the selected channel. If the approval strategy is set to *Manual*, you must manually approve pending updates.

.Prerequisites

- An Operator previously installed using Operator Lifecycle Manager (OLM).

.Procedure

1. In web console, navigate to *Ecosystem* -> *Installed Operators*.

1. Click the name of the Operator you want to change the update channel for.

1. Click the *Subscription* tab.

1. Click the name of the update channel under *Update channel*.

1. Click the newer update channel that you want to change to, then click *Save*.

1. For subscriptions with an *Automatic* approval strategy, the update begins automatically. Navigate back to the *Ecosystem* -> *Installed Operators* page to monitor the progress of the update. When complete, the status changes to *Succeeded* and *Up to date*.
For subscriptions with a *Manual* approval strategy, you can manually approve the update from the *Subscription* tab.
# Red Hat Marketplace features

Cluster administrators can use [the Red Hat Marketplace](https://marketplace.redhat.com/en-us/documentation/getting-started) to manage software on OpenShift Container Platform, give developers self-service access to deploy application instances, and correlate application usage against a quota.

## Connect OpenShift Container Platform clusters to the Marketplace

Cluster administrators can install a common set of applications on OpenShift Container Platform clusters that connect to the Marketplace. They can also use the Marketplace to track cluster usage against subscriptions or quotas. Users that they add by using the Marketplace have their product usage tracked and billed to their organization.

During the [cluster connection process](https://marketplace.redhat.com/en-us/documentation/clusters),
a Marketplace Operator is installed that updates the image registry secret, manages the catalog, and reports application usage.

## Install applications

Cluster administrators can [install Marketplace applications](https://marketplace.redhat.com/en-us/documentation/operators) from within the software catalog in OpenShift Container Platform, or from the [Marketplace web application](https://marketplace.redhat.com).

You can access installed applications from the web console by clicking *Ecosystem* -> *Installed Operators*.

## Deploy applications from different perspectives

Developers can access newly installed capabilities and deploy Marketplace applications from the web console.

For example, after a database Operator is installed, a developer can create an instance from the catalog within their project. Database usage is aggregated and reported to the cluster administrator.

Cluster administrators can access Operator installation and application usage information. They can also launch application instances by browsing custom resource definitions (CRDs) in the *Installed Operators* list.
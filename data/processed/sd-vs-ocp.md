# Understanding how OpenShift Container Platform differs from {OCP}

OpenShift Container Platform uses the same code base as {OCP} but is installed in an opinionated way to be optimized for performance, scalability, and security. OpenShift Container Platform is a fully managed service; therefore, many of the OpenShift Container Platform components and settings that you manually set up in {OCP} are set up for you by default.

Review the following differences between OpenShift Container Platform and a standard installation of {OCP} on your own infrastructure:

[options="header"]
|====
|{OCP} |OpenShift Container Platform

|The customer installs and configures {OCP}.
|

|Customers can choose their computing resources.
|

|Customers have top-level administrative access to the infrastructure.
|

|Customers can use all supported features and configuration settings available in {OCP}.
|Some {OCP} features and configuration settings might not be available or changeable in OpenShift Container Platform.

|You set up control plane components such as the API server and etcd on machines that get the `control` role. You can modify the control plane components, but are responsible for backing up, restoring, and making control plane data highly available.
|Red Hat sets up the control plane and manages the control plane components for you. The control plane is highly available.

|You are responsible for updating the underlying infrastructure for the control plane and worker nodes. You can use the OpenShift web console to update {OCP} versions.
|Red Hat automatically notifies the customer when updates are available. You can manually or automatically schedule updates in OpenShift Cluster Manager.

|Support is provided based on the terms of your Red Hat subscription or cloud provider.
|Engineered, operated, and supported by Red Hat with a 99.95% uptime SLA and 24x7 coverage. For details, see [Red Hat Enterprise Agreement Appendix 4 (Online Subscription Services)](https://www.redhat.com/licenses/Appendix-4-Red-Hat-Online-Services-20230523.pdf).

|====
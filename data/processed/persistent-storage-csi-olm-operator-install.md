# Installing the {FeatureName} CSI Driver Operator

The {FeatureName} CSI Driver Operator (a Red Hat Operator) is not installed in OpenShift Container Platform by default. Use the following procedure to install and configure the {FeatureName} CSI Driver Operator in your cluster.

// The following ifeval and restricted ifdef statements exclude STS and a note about avoiding
// installing community operator content for CSI drivers other than EWS

.Prerequisites
- Access to the OpenShift Container Platform web console.

.Procedure
To install the {FeatureName} CSI Driver Operator from the web console:

1. Log in to the web console.

1. Install the {FeatureName} CSI Operator:

.. Click *Ecosystem* -> *Software Catalog*.

.. Locate the {FeatureName} CSI Operator by typing *{FeatureName} CSI* in the filter box.

.. Click the *{FeatureName} CSI Driver Operator* button.

.. On the *{FeatureName} CSI Driver Operator* page, click *Install*.

.. On the *Install Operator* page, ensure that:
- *All namespaces on the cluster (default)* is selected.
- *Installed Namespace* is set to *openshift-cluster-csi-drivers*.

.. Click *Install*.
After the installation finishes, the {FeatureName} CSI Operator is listed in the *Installed Operators* section of the web console.

// The following ifeval statements exclude STS and a note about avoiding
// installing community operator content for CSI drivers other than EWS
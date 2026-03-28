# Installing the Google Cloud Filestore CSI Driver Operator

The Google Compute Platform (Google Cloud) Filestore Container Storage Interface (CSI) Driver Operator is not installed in OpenShift Container Platform by default.
Use the following procedure to install the Google Cloud Filestore CSI Driver Operator in your cluster.

.Prerequisites
- Access to the OpenShift Container Platform web console.
- If using GCP Workload Identity, certain GCP Workload Identity parameters are needed. See the preceding Section _Preparing to install the Google Cloud Filestore CSI Driver Operator with Workload Identity_.

.Procedure
To install the Google Cloud Filestore CSI Driver Operator from the web console:

1. Log in to the web console.

1. Enable the Filestore API in the GCE project by running the following command:
```command
$ gcloud services enable file.googleapis.com  --project <my_gce_project> <1>
```
<1> Replace `<my_gce_project>` with your Google Cloud project.
You can also do this using Google Cloud web console.

1. Install the Google Cloud Filestore CSI Operator:

.. Click *Ecosystem* -> *Software Catalog*.

.. Locate the Google Cloud Filestore CSI Operator by typing *Google Cloud Filestore* in the filter box.

.. Click the *Google Cloud Filestore CSI Driver Operator* button.

.. On the *Google Cloud Filestore CSI Driver Operator* page, click *Install*.

.. On the *Install Operator* page, ensure that:
- *All namespaces on the cluster (default)* is selected.
- *Installed Namespace* is set to *openshift-cluster-csi-drivers*.
If using GCP Workload Identity, enter values for the following fields obtained from the procedure in Section _Preparing to install the Google Cloud Filestore CSI Driver Operator with Workload Identity_:
- *Google Cloud Project Number*
- *Google Cloud Pool ID* 
- *Google Cloud Provider ID* 
- *Google Cloud Service Account Email* 

.. Click *Install*.
After the installation finishes, the Google Cloud Filestore CSI Operator is listed in the *Installed Operators* section of the web console.

1. Install the Google Cloud Filestore CSI Driver:

.. Click *administration* → *CustomResourceDefinitions* → *ClusterCSIDriver*.

.. On the *Instances* tab, click *Create ClusterCSIDriver*.
Use the following YAML file:
```yaml
apiVersion: operator.openshift.io/v1
kind: ClusterCSIDriver
metadata:
    name: filestore.csi.storage.gke.io
spec:
  managementState: Managed
```

.. Click *Create*.
.. Wait for the following Conditions to change to a "true" status:

- GCPFilestoreDriverCredentialsRequestControllerAvailable

- GCPFilestoreDriverNodeServiceControllerAvailable

- GCPFilestoreDriverControllerServiceControllerAvailable
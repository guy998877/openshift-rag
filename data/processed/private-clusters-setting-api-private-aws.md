# Restricting the API server to private for an Amazon Web Services cluster

If the security posture of your organization does not allow clusters to use an open API endpoint, you can restrict the API server to use only internal load balancers.
To implement this API server restriction, use the Amazon Web Services (AWS) console and OpenShift CLI (`oc`) to delete the external load balancer components.

.Prerequisites

- You have installed an OpenShift Container Platform cluster on AWS.
- You have access to the AWS console as a user with administrator privileges.
- You have access to the pass:quotes[OpenShift CLI (`oc`)] as a user with administrator privileges.

.Procedure

1. Log in to the AWS console as a user with administrator privileges.

1. Delete the external load balancer.
> **NOTE:** The API DNS entry in the private zone already points to the internal load balancer, which uses an identical configuration, so you do not need to modify the internal load balancer.

1. Delete the `api.<cluster_name>.<domain_name>` DNS entry in the public zone.
where `<cluster_name>` is the name of the cluster and `<domain_name>` is the base domain for the cluster.

1. To remove the external load balancers, log in to the pass:quotes[OpenShift CLI (`oc`)] as a user with administrator privileges.

1. Edit the `ControlPlaneMachineSet` CR by running the following command:
```bash
$ oc edit controlplanemachineset.machine.openshift.io cluster \
  -n openshift-machine-api
```

1. Remove the external load balancers by deleting the corresponding lines in the control plane machine set custom resource (CR).
In the `spec.template.spec.providerSpec.value.loadBalancers` section of the CR, the `name` value for the external load balancer ends in `-ext`.
Delete the line with the external load balancer `name` value and the the line with the external load balancer `type` value that accompanies it.
```yaml
apiVersion: machine.openshift.io/v1
kind: ControlPlaneMachineSet
metadata:
  name: cluster
  namespace: openshift-machine-api
spec:
# ...
  template:
# ...
      spec:
        providerSpec:
          value:
            loadBalancers:
            - name: <cluster_id>-ext
              type: network
            - name: <cluster_id>-int
              type: network
# ...
```

1. Save your changes and exit the object specification.
When you save an update to the control plane machine set, the Control Plane Machine Set Operator updates the control plane machines according to your configured update strategy.
For more information, see "Updating the control plane configuration".
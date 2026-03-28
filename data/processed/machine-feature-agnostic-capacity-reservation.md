# Capacity Reservation configuration options

OpenShift Container Platform version 4.21 and later supports
ifdef::azure[on-demand Capacity Reservation with Capacity Reservation groups on Microsoft Azure clusters.]
ifdef::aws[Capacity Reservations on Amazon Web Services clusters, including On-Demand Capacity Reservations and Capacity Blocks for ML.]

You can deploy machines on any available resources that match the parameters of a capacity request that you define.
These parameters specify the 
ifdef::azure[VM size,]
ifdef::aws[instance type,]
region, and number of instances that you want to reserve.
If your 
ifdef::azure[Azure subscription quota]
ifdef::aws[Capacity Reservation]
can accommodate the capacity request, the deployment succeeds.

> **NOTE:** You cannot change an existing Capacity Reservation configuration for a machine set. To use a different Capacity Reservation group, you must replace the machine set and the machines that the previous machine set deployed.

.Sample Capacity Reservation configuration
```yaml
apiVersion: infrastructure.cluster.x-k8s.io/v1beta2
kind: AWSMachineTemplate
# ...
spec:
  template:
    spec:
      capacityReservationId: <capacity_reservation> # <1>
      capacityReservationPreference: <reservation_preference> # <2>
      marketType: <market_type> # <3>
# ...
```
<1> Specify the ID of the 
ifdef::azure[Capacity Reservation group]
ifdef::aws[Capacity Block for ML or On-Demand Capacity Reservation]
that you want to deploy machines on.

For more information, including limitations and suggested use cases for this offering, see
ifdef::azure[[On-demand Capacity Reservation](https://learn.microsoft.com/en-us/azure/virtual-machines/capacity-reservation-overview) in the Microsoft Azure documentation.]
ifdef::aws[[On-Demand Capacity Reservations and Capacity Blocks for ML](https://docs.aws.amazon.com/en_us/AWSEC2/latest/UserGuide/capacity-reservation-overview.html) in the AWS documentation.]
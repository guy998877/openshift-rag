# Troubleshooting cluster creation with an InvalidInstallConfigSubnet error

If a cluster creation action fails, you might receive the following error messages.

.Example install logs output
```bash
platform.aws.subnets[1]: Invalid value: "subnet-0babad72exxxxxxxx": subnet's CIDR range start 10.69.1x.3x is outside of the specified machine networks
```

.Example OpenShift Cluster Manager output
```bash
Provisioning Error Code:    OCM3020
Provisioning Error Message: Subnet CIDR ranges are outside of specified machine CIDR.
```

These errors indicate that a subnet's CIDR range start is outside of the specified machine networks.

.Procedure

1. Check your subnet configuration.
1. Edit your machine CIDR range to include all subnet CIDR ranges. Generally, your machine CIDR should match your VPC CIDR.
For more information about CIDR ranges, see _CIDR range definitions_ in the _Additional resources_ section .
# Troubleshooting cluster creation with an AWSInsufficientCapacity error

If a cluster creation action fails, you might receive the following error message.

.Example output
```bash
Provisioning Error Code:    OCM3052
Provisioning Error Message: AWSInsufficientCapacity.
```

This error indicates that AWS has run out of capacity for a particular availability zone that you have requested.

.Procedure

- Try reinstalling or select a different AWS region or different availability zones.
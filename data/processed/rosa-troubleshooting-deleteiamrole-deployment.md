# Troubleshooting cluster creation with a DeletingIAMRole error

If a cluster creation action fails, you might receive the following error message.

.Example output
```bash
OCM3031: Error deleting IAM Role (role-name): DeleteConflict: Cannot delete entity, must detach all policies first.\nlevel=error msg=\tstatus code: 409
```

The cluster's installation was blocked as the cluster installer was not able to delete the roles it used during the installation.

.Procedure

- To unblock the cluster installation, ensure that no policies are added to new roles by default by running the following command to list all managed policies that are attached to the specified role:
```bash
$ aws iam list-attached-role-policies --role-name <role-name>
```
.Example output
```bash
{
  "AttachedPolicies": [
    {
      "PolicyName": "SecurityAudit",
      "PolicyArn": "arn:aws:iam::aws:policy/SecurityAudit"
    }
  ],
  "IsTruncated": false
}
```
If there are no policies attached to the specified role (or none that match the specified path prefix), the command returns an empty list.
For more information about the list-attached-role-policies command, see [list-attached-role-policies](https://docs.aws.amazon.com/cli/latest/reference/iam/list-attached-role-policies.html) in the official AWS documentation.
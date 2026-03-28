# Troubleshooting cluster creation with an osdCcsAdmin error

If a cluster creation action fails, you might receive the following error message.

.Example output
```bash
Failed to create cluster: Unable to create cluster spec: Failed to get access keys for user 'osdCcsAdmin': NoSuchEntity: The user with name osdCcsAdmin cannot be found.
```

.Procedure

1. Delete the stack:
```bash
$ rosa init --delete
```
1. Reinitialize your account:
```bash
$ rosa init
```
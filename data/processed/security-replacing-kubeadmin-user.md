# Replacing the kubeadmin user with a cluster-admin user

The `kubeadmin` user with the `cluster-admin` privileges is created on every cluster by default. To enhance the cluster security, you can replace the`kubeadmin` user with a `cluster-admin` user and then disable or remove the `kubeadmin` user.

.Prerequisites

- You have created a user with `cluster-admin` privileges.
- You have installed the OpenShift CLI (`oc`).
- You have administrative access to a virtual vault for secure storage.

.Procedure

1. Create an emergency `cluster-admin` user by using the `htpasswd` identity provider. For more information, see "About htpasswd authentication".

1. Assign the `cluster-admin` privileges to the new user by running the following command:
```bash
$ oc adm policy add-cluster-role-to-user cluster-admin <emergency_user>
```

1. Verify the emergency user access:

.. Log in to the cluster using the new emergency user.
.. Confirm that the user has `cluster-admin` privileges by running the following command:
```bash
$ oc whoami
```
Ensure the output shows the ID of the emergency user.

1. Store the password or authentication key for the emergency user securely in a virtual vault. 
> **NOTE:** Follow the best practices of your organization for securing sensitive credentials.

1. Disable or remove the `kubeadmin` user to reduce security risks by running the following command:
```bash
$ oc delete secrets kubeadmin -n kube-system
```
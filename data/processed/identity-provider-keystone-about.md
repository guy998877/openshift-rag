# About Keystone authentication

[Keystone](http://docs.openstack.org/developer/keystone/) is an OpenStack project that provides identity, token, catalog, and policy services.

You can configure the integration with Keystone so that the new OpenShift Container Platform users are based on either the Keystone user names or unique Keystone IDs. With both methods, users log in by entering their Keystone user name and password. Basing the OpenShift Container Platform users on the Keystone ID is more secure because if you delete a Keystone user and create a new Keystone user with that user name, the new user might have access to the old user's resources.
# About htpasswd authentication

Using htpasswd authentication in OpenShift Container Platform allows you to identify users based on an htpasswd file. An htpasswd file is a flat file that contains the user name and hashed password for each user. You can use the `htpasswd` utility to create this file.

> **WARNING:** Do not use htpasswd authentication in OpenShift Container Platform for production environments. Use htpasswd authentication only for development environments.
# Creating an htpasswd file using Linux

To use the htpasswd identity provider, you must generate a flat file that
contains the user names and passwords for your cluster by using
[`htpasswd`](http://httpd.apache.org/docs/2.4/programs/htpasswd.html).

.Prerequisites

- Have access to the `htpasswd` utility. On Red Hat Enterprise Linux
this is available by installing the `httpd-tools` package.

.Procedure

1. Create or update your flat file with a user name and hashed password:
```bash
$ htpasswd -c -B -b </path/to/users.htpasswd> <username> <password>
```
The command generates a hashed version of the password.
For example:
```bash
$ htpasswd -c -B -b users.htpasswd <username> <password>
```
.Example output
```bash
Adding password for user user1
```

1. Continue to add or update credentials to the file:
```bash
$ htpasswd -B -b </path/to/users.htpasswd> <user_name> <password>
```
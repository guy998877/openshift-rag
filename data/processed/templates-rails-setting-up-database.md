# Setting up the database

Rails applications are almost always used with a database. For local development use the PostgreSQL database.

.Procedure

1. Install the database:
```bash
$ sudo yum install -y postgresql postgresql-server postgresql-devel
```

1. Initialize the database:
```bash
$ sudo postgresql-setup initdb
```
This command creates the `/var/lib/pgsql/data` directory, in which the data is stored.

1. Start the database:
```bash
$ sudo systemctl start postgresql.service
```

1. When the database is running, create your `rails` user:
```bash
$ sudo -u postgres createuser -s rails
```
Note that the user created has no password.
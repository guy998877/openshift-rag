# Migrating SQLite database catalogs to the file-based catalog format

You can update your deprecated SQLite database format catalogs to the file-based catalog format.

.Prerequisites

- You have a SQLite database catalog source.
- You have access to the cluster as a user with the `cluster-admin` role.
- You have the latest version of the `opm` CLI tool released with OpenShift Container Platform 
4.21 
on your workstation.

.Procedure

1. Migrate your SQLite database catalog to a file-based catalog by running the following command:
```bash
$ opm migrate <registry_image> <fbc_directory>
```

1. Generate a Dockerfile for your file-based catalog by running the following command:
```bash
$ opm generate dockerfile <fbc_directory> \
  --binary-image \
  registry.redhat.io/openshift4/ose-operator-registry-rhel9:v4.21
```

.Next steps

- The generated Dockerfile can be built, tagged, and pushed to your registry.
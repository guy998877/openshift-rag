# Configuring an htpasswd identity provider with an htpasswd file

You can create an htpasswd identity provider (IDP) with the {rosa-cli-first} tool and a well-formed htpasswd file.

.Prerequisites

- You have installed and configured the latest version of the {rosa-cli}.

.Procedure

- Create a text file with a new row for each set of credentials with the username and password being colon separated like the following example:
```text
johndoe:$apr1$hRY7OJWH$km1EYH.UIRj00000000/
janedoe:$apr1$Q58SO804$B/fECNWfn5F00000000/
```
> **NOTE:** The htpasswd file is encrypted using APR1 hashing. For more information, see "Apache Password Formats" in the _Additional resources_.
```bash
$ rosa create idp --type=htpasswd -c <cluster_name> --from-file=myhtpassfile.txt
```
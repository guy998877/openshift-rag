# Impersonating the system:admin group

When a `system:admin` user is granted cluster administration permissions through a group, you must include the
`--as=<user> --as-group=<group1> --as-group=<group2>` parameters in the command to impersonate the associated groups.

.Procedure

- To grant a user permission to impersonate a `system:admin` by impersonating the associated cluster administration groups,
run the following command:
```bash
$ oc create clusterrolebinding <any_valid_name> --clusterrole=sudoer --as=<user> \
--as-group=<group1> --as-group=<group2>
```
# About the augmented Active Directory configuration file

The augmented Active Directory schema requires you to provide an LDAP query
definition for both user entries and group entries, as well as the attributes
with which to represent them in the internal OpenShift Container Platform group records.

For clarity, the group you create in OpenShift Container Platform should use attributes other
than the distinguished name whenever possible for user- or administrator-facing
fields. For example, identify the users of an OpenShift Container Platform group by their e-mail,
and use the name of the group as the common name. The following configuration
file creates these relationships.

.LDAP sync configuration that uses augmented Active Directory schema: `augmented_active_directory_config.yaml`
```yaml
kind: LDAPSyncConfig
apiVersion: v1
url: ldap://LDAP_SERVICE_IP:389
augmentedActiveDirectory:
    groupsQuery:
        baseDN: "ou=groups,dc=example,dc=com"
        scope: sub
        derefAliases: never
        pageSize: 0
    groupUIDAttribute: dn <1>
    groupNameAttributes: [ cn ] <2>
    usersQuery:
        baseDN: "ou=users,dc=example,dc=com"
        scope: sub
        derefAliases: never
        filter: (objectclass=person)
        pageSize: 0
    userNameAttributes: [ mail ] <3>
    groupMembershipAttributes: [ memberOf ] <4>
```
<1> The attribute that uniquely identifies a group on the LDAP server. You
cannot specify `groupsQuery` filters when using DN for groupUIDAttribute. For
fine-grained filtering, use the whitelist / blacklist method.
<2> The attribute to use as the name of the group.
<3> The attribute to use as the name of the user in the OpenShift Container Platform group record.
<4> The attribute on the user that stores the membership information.
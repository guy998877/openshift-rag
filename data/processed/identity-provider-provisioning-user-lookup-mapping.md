# Manually provisioning a user when using the lookup mapping method

Typically, identities are automatically mapped to users during login. The `lookup` mapping method disables this automatic mapping, which requires you to provision users manually. If you are using the `lookup` mapping method, use the following procedure for each user after configuring the identity provider.

.Prerequisites

- You have installed the pass:quotes[OpenShift CLI (`oc`)].

.Procedure

1. Create an OpenShift Container Platform user:
```bash
$ oc create user <username>
```

1. Create an OpenShift Container Platform identity:
```bash
$ oc create identity <identity_provider>:<identity_provider_user_id>
```
Where `<identity_provider_user_id>` is a name that uniquely represents the user in the identity provider.

1. Create a user identity mapping for the created user and identity:
```bash
$ oc create useridentitymapping <identity_provider>:<identity_provider_user_id> <username>
```
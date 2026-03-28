# Understanding identity providers

OpenShift Container Platform includes a built-in OAuth server. Developers and administrators obtain OAuth access tokens to authenticate themselves to the API. As an administrator, you can configure OAuth to specify an identity provider after you install your cluster. Configuring identity providers allows users to log in and access the cluster.

## Supported identity providers
// This section is sourced from authentication/understanding-identity-provider.adoc

You can configure the following types of identity providers:

[cols="2a,8a",options="header"]
|===

|Identity provider
|Description

|GitHub or GitHub Enterprise
|Configure a GitHub identity provider to validate usernames and passwords against GitHub or GitHub Enterprise's OAuth authentication server.

|GitLab
|Configure a GitLab identity provider to use [GitLab.com](https://gitlab.com/) or any other GitLab instance as an identity provider.

|Google
|Configure a Google identity provider using [Google's OpenID Connect integration](https://developers.google.com/identity/protocols/OpenIDConnect).

|LDAP
|Configure an LDAP identity provider to validate usernames and passwords against an LDAPv3 server, using simple bind authentication.

|OpenID Connect
|Configure an OpenID Connect (OIDC) identity provider to integrate with an OIDC identity provider using an [Authorization Code Flow](http://openid.net/specs/openid-connect-core-1_0.html#CodeFlowAuth).

|htpasswd
|Configure an htpasswd identity provider for a single, static administration user. You can log in to the cluster as the user to troubleshoot issues.

> **IMPORTANT:** The htpasswd identity provider option is included only to enable the creation of a single, static administration user. htpasswd is not supported as a general-use identity provider for OpenShift Container Platform. For the steps to configure the single user, see _Configuring an htpasswd identity provider_.

|===
# Configuring an OpenID identity provider

Configure an OpenID identity provider to integrate with an OpenID Connect identity provider using an [Authorization Code Flow](http://openid.net/specs/openid-connect-core-1_0.html#CodeFlowAuth).

> **IMPORTANT:** The Authentication Operator in OpenShift Container Platform requires that the configured OpenID Connect identity provider implements the link:https://openid.net/specs/openid-connect-discovery-1_0.html[OpenID Connect Discovery] specification.

Claims are read from the JWT `id_token` returned from the OpenID identity
provider and, if specified, from the JSON returned by the Issuer URL.

At least one claim must be configured to use as the user's identity.

You can also indicate which claims to use as the user's preferred user name,
display name, and email address. If multiple claims are specified, the first one
with a non-empty value is used. The standard claims are:

[cols="1,2",options="header"]
|===

|Claim
|Description

|`preferred_username`
|The preferred user name when provisioning a user. A
shorthand name that the user wants to be referred to as, such as `janedoe`. Typically
a value that corresponding to the user's login or username in the authentication
system, such as username or email.

|`email`
|Email address.

|`name`
|Display name.

|===

See the
[OpenID claims documentation](http://openid.net/specs/openid-connect-core-1_0.html#StandardClaims)
for more information.

.Prerequisites
- Before you configure OpenID Connect, check the installation prerequisites for any Red Hat product or service you want to use with your OpenShift Container Platform cluster.

.Procedure

1. From link:https://console.redhat.com/openshift[OpenShift Cluster Manager], navigate to the *Cluster List* page and select the cluster that you need to configure identity providers for.

1. Click the *Access control* tab.

1. Click *Add identity provider*.
> **NOTE:** You can also click the *Add Oauth configuration* link in the warning message displayed after cluster creation to configure your identity providers.

1. Select *OpenID* from the drop-down menu.

1. Enter a unique name for the identity provider. This name cannot be changed later.
- An *OAuth callback URL* is automatically generated in the provided field.
https://oauth-openshift.apps.<cluster_name>.<cluster_domain>/oauth2callback/<idp_provider_name>
For example:
https://oauth-openshift.apps.openshift-cluster.example.com/oauth2callback/openid

1. Register a new OpenID Connect client in the OpenID identity provider by following the steps to link:https://openid.net/specs/openid-connect-core-1_0.html#AuthRequest[create an authorization request].

1. Return to OpenShift Container Platform and select a mapping method from the drop-down menu. *Claim* is recommended in most cases.

1. Enter a *Client ID* and *Client secret* provided from OpenID.

1. Enter an *Issuer URL*. This is the URL that the OpenID provider asserts as the Issuer Identifier. It must use the https scheme with no URL query parameters or fragments.

1. Enter an *Email* attribute whose value should be used as the email address. Click *Add more* to add multiple email attributes.

1. Enter a *Name* attribute whose value should be used as the preferred username. Click *Add more* to add multiple preferred usernames.

1. Enter a *Preferred username* attribute whose value should be used as the display name. Click *Add more* to add multiple display names.

1. Optional: Click *Show advanced Options* to add a certificate authority (CA) file to your OpenID identity provider.

1. Optional: Under the advanced options, you can add *Additional scopes*. By default, the `OpenID` scope is requested.

1. Click *Confirm*.

.Verification

- The configured identity provider is now visible on the *Access control* tab of the *Cluster List* page.
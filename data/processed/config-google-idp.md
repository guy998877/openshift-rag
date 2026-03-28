# Configuring a Google identity provider

Configure a Google identity provider to allow users to authenticate with their Google credentials.

> **WARNING:** Using Google as an identity provider allows any Google user to authenticate to your server. You can limit authentication to members of a specific hosted domain with the `hostedDomain` configuration attribute.

.Procedure

1. From link:https://console.redhat.com/openshift[OpenShift Cluster Manager], navigate to the *Cluster List* page and select the cluster that you need to configure identity providers for.

1. Click the *Access control* tab.

1. Click *Add identity provider*.
> **NOTE:** You can also click the *Add Oauth configuration* link in the warning message displayed after cluster creation to configure your identity providers.

1. Select *Google* from the drop-down menu.

1. Enter a unique name for the identity provider. This name cannot be changed later.
- An *OAuth callback URL* is automatically generated in the provided field. You will provide this URL to Google.
https://oauth-openshift.apps.<cluster_name>.<cluster_domain>/oauth2callback/<idp_provider_name>
For example:
https://oauth-openshift.apps.openshift-cluster.example.com/oauth2callback/google

1. Configure a Google identity provider using link:https://developers.google.com/identity/protocols/OpenIDConnect[Google's OpenID Connect integration].

1. Return to OpenShift Container Platform and select a mapping method from the drop-down menu. *Claim* is recommended in most cases.

1. Enter the *Client ID* of a registered Google project and the *Client secret* issued by Google.

1. Enter a hosted domain to restrict users to a Google Apps domain.

1. Click *Confirm*.

.Verification

- The configured identity provider is now visible on the *Access control* tab of the *Cluster List* page.
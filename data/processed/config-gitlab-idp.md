# Configuring a GitLab identity provider

Configure a GitLab identity provider to use [GitLab.com](https://gitlab.com/) or any other GitLab instance as an identity provider.

.Prerequisites

- If you use GitLab version 7.7.0 to 11.0, you connect using the [OAuth integration](http://doc.gitlab.com/ce/integration/oauth_provider.html). If you use GitLab version 11.1 or later, you can use [OpenID Connect](https://docs.gitlab.com/ce/integration/openid_connect_provider.html) (OIDC) to connect instead of OAuth.

.Procedure

1. From link:https://console.redhat.com/openshift[OpenShift Cluster Manager], navigate to the *Cluster List* page and select the cluster that you need to configure identity providers for.

1. Click the *Access control* tab.

1. Click *Add identity provider*.
> **NOTE:** You can also click the *Add Oauth configuration* link in the warning message displayed after cluster creation to configure your identity providers.

1. Select *GitLab* from the drop-down menu.

1. Enter a unique name for the identity provider. This name cannot be changed later.
- An *OAuth callback URL* is automatically generated in the provided field. You will provide this URL to GitLab.
https://oauth-openshift.apps.<cluster_name>.<cluster_domain>/oauth2callback/<idp_provider_name>
For example:
https://oauth-openshift.apps.openshift-cluster.example.com/oauth2callback/gitlab

1. link:https://docs.gitlab.com/ee/integration/oauth_provider.html[Add a new application in GitLab].

1. Return to OpenShift Container Platform and select a mapping method from the drop-down menu. *Claim* is recommended in most cases.

1. Enter the *Client ID* and *Client secret* provided by GitLab.

1. Enter the *URL* of your GitLab provider.

1. Optional: You can use a certificate authority (CA) file to validate server certificates for the configured GitLab URL. Click *Browse* to locate and attach a *CA file* to the identity provider.

1. Click *Confirm*.

.Verification

- The configured identity provider is now visible on the *Access control* tab of the *Cluster List* page.
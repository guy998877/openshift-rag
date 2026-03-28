# Supported OIDC providers

Red Hat tests and supports specific OpenID Connect (OIDC) providers with OpenShift Container Platform. The following OpenID Connect (OIDC) providers are tested and supported with OpenShift Container Platform. Using an OIDC provider that is not on the following list might work with OpenShift Container Platform, but the provider was not tested by Red Hat and therefore is not supported by Red Hat.

- Active Directory Federation Services for Windows Server
> **NOTE:** Currently, it is not supported to use Active Directory Federation Services for Windows Server with OpenShift Container Platform when custom claims are used.
- GitLab
- Google
- Keycloak
- Microsoft Entra ID
> **NOTE:** Currently, it is not supported to use Microsoft Entra ID when group names are required to be synced.
- Okta
- Ping Identity
- Red Hat Single Sign-On
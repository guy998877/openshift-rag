// Module included in the following assemblies:
//
// * support/rosa-troubleshooting-expired-tokens.adoc

# Troubleshooting expired offline access tokens

If you use the OpenShift Container Platform (ROSA) CLI, `rosa`, and your api.openshift.com offline access token expires, an error message appears. This happens when sso.redhat.com invalidates the token.

.Example output
```bash
Can't get tokens ....
Can't get access tokens ....
```

.Procedure
- Generate a new offline access token at the following URL. A new offline access token is generated every time you visit the link:https://console.redhat.com/openshift[OpenShift Cluster Manager] URL.
# Registering a GitHub application

To use GitHub or GitHub Enterprise as an identity provider, you must register
an application to use.

.Procedure

1. Register an application on GitHub:
- For GitHub, click https://github.com/settings/profile[*Settings*] ->
https://github.com/settings/apps[*Developer settings*] ->
https://github.com/settings/developers[*OAuth Apps*] ->
https://github.com/settings/applications/new[*Register a new OAuth application*].
- For GitHub Enterprise, go to your GitHub Enterprise home page and then click
*Settings -> Developer settings -> Register a new application*.
1. Enter an application name, for example `My OpenShift Install`.
1. Enter a homepage URL, such as
`\https://oauth-openshift.apps.<cluster-name>.<cluster-domain>`.
1. Optional: Enter an application description.
1. Enter the authorization callback URL, where the end of the URL contains the
identity provider `name`:
https://oauth-openshift.apps.<cluster-name>.<cluster-domain>/oauth2callback/<idp-provider-name>
For example:
https://oauth-openshift.apps.openshift-cluster.example.com/oauth2callback/github
1. Click *Register application*. GitHub provides a client ID and a client secret.
You need these values to complete the identity provider configuration.
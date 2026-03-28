# Installing a Helm chart on an OpenShift Container Platform cluster

.Prerequisites
- You have a running OpenShift Container Platform cluster and you have logged into it.
- You have installed Helm.

.Procedure

1. Create a new project:
```bash
$ oc new-project vault
```

1. Add a repository of Helm charts to your local Helm client:
```bash
$ helm repo add openshift-helm-charts https://charts.openshift.io/
```
.Example output
```bash
"openshift-helm-charts" has been added to your repositories
```

1. Update the repository:
```bash
$ helm repo update
```

1. Install an example HashiCorp Vault:
```bash
$ helm install example-vault openshift-helm-charts/hashicorp-vault
```
.Example output
```bash
NAME: example-vault
LAST DEPLOYED: Fri Mar 11 12:02:12 2022
NAMESPACE: vault
STATUS: deployed
REVISION: 1
NOTES:
Thank you for installing HashiCorp Vault!
```

1. Verify that the chart has installed successfully:
```bash
$ helm list
```
.Example output
```bash
NAME         	NAMESPACE	REVISION	UPDATED                                	STATUS  	CHART       	APP VERSION
example-vault	vault    	1       	2022-03-11 12:02:12.296226673 +0530 IST	deployed	vault-0.19.0	1.9.2
```
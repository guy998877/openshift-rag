# Configuring the COS instance

You create an IBM Cloud Object Storage (COS) instance to store the OADP backup data. After you create the COS instance, configure the `HMAC` service credentials.

.Prerequisites

- You have an IBM Cloud Platform account.
- You installed the link:https://cloud.ibm.com/docs/cli?topic=cli-getting-started[IBM Cloud CLI].
- You are logged in to IBM Cloud.

.Procedure

1. Install the IBM Cloud Object Storage (COS) plugin by running the following command:
```bash
$ ibmcloud plugin install cos -f
```

1. Set a bucket name by running the following command:
```bash
$ BUCKET=<bucket_name>
```

1. Set a bucket region by running the following command:
```bash
$ REGION=<bucket_region>
```
where:
`<bucket_region>`:: Specifies the bucket region. For example, `eu-gb`.

1. Create a resource group by running the following command:
```bash
$ ibmcloud resource group-create <resource_group_name>
```

1. Set the target resource group by running the following command:
```bash
$ ibmcloud target -g <resource_group_name>
```

1. Verify that the target resource group is correctly set by running the following command: 
```bash
$ ibmcloud target
```
.Example output

```yaml
API endpoint:     https://cloud.ibm.com
Region:           
User:             test-user
Account:          Test Account (fb6......e95) <-> 2...122
Resource group:   Default
```
In the example output, the resource group is set to `Default`.

1. Set a resource group name by running the following command:
```bash
$ RESOURCE_GROUP=<resource_group>
```
where:
`<resource_group>`:: Specifies the resource group name. For example, `"default"`.

1. Create an IBM Cloud `service-instance` resource  by running the following command:
```bash
$ ibmcloud resource service-instance-create \
<service_instance_name> \
<service_name> \
<service_plan> \
<region_name>
```
where:
`<service_instance_name>`:: Specifies a name for the `service-instance` resource.
`<service_name>`:: Specifies the service name. Alternatively, you can specify a service ID.
`<service_plan>`:: Specifies the service plan for your IBM Cloud account.
`<region_name>`:: Specifies the region name. 

--
Refer to the following example command:

```bash
$ ibmcloud resource service-instance-create test-service-instance cloud-object-storage \
standard \
global \
-d premium-global-deployment
```
where:

`cloud-object-storage`:: Specifies the service name.
`-d premium-global-deployment`:: Specifies the deployment name.
--

1. Extract the service instance ID by running the following command:
```bash
$ SERVICE_INSTANCE_ID=$(ibmcloud resource service-instance test-service-instance --output json | jq -r '.[0].id')
```

1. Create a COS bucket by running the following command: 
```bash
$ ibmcloud cos bucket-create \
--bucket $BUCKET \
--ibm-service-instance-id $SERVICE_INSTANCE_ID \
--region $REGION 
```
Variables such as `$BUCKET`, `$SERVICE_INSTANCE_ID`, and `$REGION` are replaced by the values you set previously.

1. Create `HMAC` credentials by running the following command.
```bash
$ ibmcloud resource service-key-create test-key Writer --instance-name test-service-instance --parameters {\"HMAC\":true}
```

1. Extract the access key ID and the secret access key from the `HMAC` credentials and save them in the `credentials-velero` file. You can use the `credentials-velero` file to create a `secret` for the backup storage location. Run the following command:
```bash
$ cat > credentials-velero << __EOF__
[default]
aws_access_key_id=$(ibmcloud resource service-key test-key -o json  | jq -r '.[0].credentials.cos_hmac_keys.access_key_id')
aws_secret_access_key=$(ibmcloud resource service-key test-key -o json  | jq -r '.[0].credentials.cos_hmac_keys.secret_access_key')
__EOF__
```
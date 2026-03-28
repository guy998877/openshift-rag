# Configuring Google Cloud

You configure a Google Cloud storage bucket as a replication repository for the Migration Toolkit for Containers (MTC).
You configure Google Cloud for the OpenShift API for Data Protection (OADP).

.Prerequisites

- You must have the `gcloud` and `gsutil` CLI tools installed. See the link:https://cloud.google.com/sdk/docs/[Google cloud documentation] for details.

- The Google Cloud storage bucket must be accessible to the source and target clusters.
- If you are using the snapshot copy method:
- The source and target clusters must be in the same region.
- The source and target clusters must have the same storage class.
- The storage class must be compatible with snapshots.

.Procedure

1. Log in to Google Cloud:
```bash
$ gcloud auth login
```

1. Set the `BUCKET` variable:
```bash
$ BUCKET=<bucket>
```
where:
`bucket`:: Specifies the bucket name.

1. Create the storage bucket:
```bash
$ gsutil mb gs://$BUCKET/
```

1. Set the `PROJECT_ID` variable to your active project:
```bash
$ PROJECT_ID=$(gcloud config get-value project)
```

1. Create a service account:
```bash
$ gcloud iam service-accounts create velero \
    --display-name "Velero service account"
```

1. List your service accounts:
```bash
$ gcloud iam service-accounts list
```

1. Set the `SERVICE_ACCOUNT_EMAIL` variable to match its `email` value:
```bash
$ SERVICE_ACCOUNT_EMAIL=$(gcloud iam service-accounts list \
    --filter="displayName:Velero service account" \
    --format 'value(email)')
```

1. Attach the policies to give the `velero` user the minimum necessary permissions:
```bash
$ ROLE_PERMISSIONS=(
    compute.disks.get
    compute.disks.create
    compute.disks.createSnapshot
    compute.snapshots.get
    compute.snapshots.create
    compute.snapshots.useReadOnly
    compute.snapshots.delete
    compute.zones.get
    storage.objects.create
    storage.objects.delete
    storage.objects.get
    storage.objects.list
    iam.serviceAccounts.signBlob
)
```

1. Create the `velero.server` custom role:
```bash
$ gcloud iam roles create velero.server \
    --project $PROJECT_ID \
    --title "Velero Server" \
    --permissions "$(IFS=","; echo "${ROLE_PERMISSIONS[*]}")"
```

1. Add IAM policy binding to the project:
```bash
$ gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member serviceAccount:$SERVICE_ACCOUNT_EMAIL \
    --role projects/$PROJECT_ID/roles/velero.server
```

1. Update the IAM service account:
```bash
$ gsutil iam ch serviceAccount:$SERVICE_ACCOUNT_EMAIL:objectAdmin gs://${BUCKET}
```

1. Save the IAM service account keys to the `credentials-velero` file in the current directory:
```bash
$ gcloud iam service-accounts keys create credentials-velero \
    --iam-account $SERVICE_ACCOUNT_EMAIL
```
You use the `credentials-velero` file to add Google Cloud as a replication repository.
You use the `credentials-velero` file to create a `Secret` object for Google Cloud before you install the Data Protection Application.
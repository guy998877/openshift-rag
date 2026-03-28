# Modifying your node tuning configurations

You can view and update the node tuning configurations by using the OpenShift Container Platform (ROSA) CLI, `rosa`.

.Prerequisites

- You have downloaded the latest version of the ROSA CLI.
- You have a cluster on the latest version
- Your cluster has a node tuning configuration added to it

.Procedure

1. You view the tuning configurations with the `rosa describe` command:
```bash
$ rosa describe tuning-config -c <cluster_id> \
       --name <name_of_tuning> \
       [-o json]
```
where:
--
`<cluster_id>`:: Specifies the cluster ID for the cluster that you own that you want to apply a node tuning configuration.
`<name_of_tuning>`:: Specifies the name of your tuning configuration.
`-o json`:: Specifies the output type. This parameter is optional. If you do not specify any outputs, you see only the ID and name of the tuning configuration.
--
.Example output without specifying output type
```bash
Name:    sample-tuning
ID:      20468b8e-edc7-11ed-b0e4-0a580a800298
Spec:    {
            "profile": [
              {
                "data": "[main]\nsummary=Custom OpenShift profile\ninclude=openshift-node\n\n[sysctl]\nvm.dirty_ratio=\"55\"\n",
                "name": "tuned-1-profile"
              }
            ],
            "recommend": [
              {
                 "priority": 20,
                 "profile": "tuned-1-profile"
              }
            ]
         }

```
.Example output specifying JSON output
```bash
{
  "kind": "TuningConfig",
  "id": "20468b8e-edc7-11ed-b0e4-0a580a800298",
  "href": "/api/clusters_mgmt/v1/clusters/23jbsevqb22l0m58ps39ua4trff9179e/tuning_configs/20468b8e-edc7-11ed-b0e4-0a580a800298",
  "name": "sample-tuning",
  "spec": {
    "profile": [
      {
        "data": "[main]\nsummary=Custom OpenShift profile\ninclude=openshift-node\n\n[sysctl]\nvm.dirty_ratio=\"55\"\n",
        "name": "tuned-1-profile"
      }
    ],
    "recommend": [
      {
        "priority": 20,
        "profile": "tuned-1-profile"
      }
    ]
  }
}
```

1. After verifying the tuning configuration, you edit the existing configurations with the `rosa edit` command:
$ rosa edit tuning-config -c <cluster_id> --name <name_of_tuning> --spec-path <path_to_spec_file>
In this command, you use the `spec.json` file to edit your configurations.

.Verification

- Run the `rosa describe` command again, to see that the changes you made to the `spec.json` file are updated in the tuning configurations:
```bash
$ rosa describe tuning-config -c <cluster_id> --name <name_of_tuning>
```
.Example output
```bash
Name:  sample-tuning
ID:    20468b8e-edc7-11ed-b0e4-0a580a800298
Spec:  {
           "profile": [
             {
              "data": "[main]\nsummary=Custom OpenShift profile\ninclude=openshift-node\n\n[sysctl]\nvm.dirty_ratio=\"55\"\n",
              "name": "tuned-2-profile"
             }
           ],
           "recommend": [
             {
              "priority": 10,
              "profile": "tuned-2-profile"
             }
           ]
       }
```
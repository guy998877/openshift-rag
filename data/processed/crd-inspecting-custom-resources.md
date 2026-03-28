# Inspecting custom resources

You can inspect custom resource (CR) objects that exist in your cluster using the CLI.

.Prerequisites

- A CR object exists in a namespace to which you have access.

.Procedure

1. To get information on a specific kind of a CR, run:
```bash
$ oc get <kind>
```
For example:
```bash
$ oc get crontab
```
.Example output
```bash
NAME                 KIND
my-new-cron-object   CronTab.v1.stable.example.com
```
Resource names are not case-sensitive, and you can use either the singular or plural forms defined in the CRD, as well as any short name. For example:
```bash
$ oc get crontabs
```
```bash
$ oc get crontab
```
```bash
$ oc get ct
```

1. You can also view the raw YAML data for a CR:
```bash
$ oc get <kind> -o yaml
```
For example:
```bash
$ oc get ct -o yaml
```
.Example output
```bash
apiVersion: v1
items:
- apiVersion: stable.example.com/v1
  kind: CronTab
  metadata:
    clusterName: ""
    creationTimestamp: 2017-05-31T12:56:35Z
    deletionGracePeriodSeconds: null
    deletionTimestamp: null
    name: my-new-cron-object
    namespace: default
    resourceVersion: "285"
    selfLink: /apis/stable.example.com/v1/namespaces/default/crontabs/my-new-cron-object
    uid: 9423255b-4600-11e7-af6a-28d2447dc82b
  spec:
    cronSpec: '* * * * /5' <1>
    image: my-awesome-cron-image <1>
```
<1> Custom data from the YAML that you used to create the object displays.
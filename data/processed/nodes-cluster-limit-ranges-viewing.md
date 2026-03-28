# Viewing a limit

You can view the limits defined in a project by navigating in the web console to the project's *Quota* page. This allows you to see details about each of the limit ranges in a project. 

You can also use the CLI to view limit range details:

.Procedure

1. Get the list of `LimitRange` objects defined in the project. For example, for a project called *demoproject*:
```bash
$ oc get limits -n demoproject
```
```bash
NAME              CREATED AT
resource-limits   2020-07-15T17:14:23Z
```

1. Describe the `LimitRange` object you are interested in, for example the `resource-limits` limit range:

```bash
$ oc describe limits resource-limits -n demoproject
```

```bash
Name:                           resource-limits
Namespace:                      demoproject
Type                            Resource                Min     Max     Default Request Default Limit   Max Limit/Request Ratio
----                            --------                ---     ---     --------------- -------------   -----------------------
Pod                             cpu                     200m    2       -               -               -
Pod                             memory                  6Mi     1Gi     -               -               -
Container                       cpu                     100m    2       200m            300m            10
Container                       memory                  4Mi     1Gi     100Mi           200Mi           -
openshift.io/Image              storage                 -       1Gi     -               -               -
openshift.io/ImageStream        openshift.io/image      -       12      -               -               -
openshift.io/ImageStream        openshift.io/image-tags -       10      -               -               -
PersistentVolumeClaim           storage                 -       50Gi    -               -               -
```
# Rolling back a Helm release

If a release fails, you can rollback the Helm release to a previous version.

.Procedure
To rollback a release using the *Helm* view:

1. In the *Developer* perspective, navigate to the *Helm* view to see the *Helm Releases* in the namespace.
1. Click the Options menu image:kebab.png[title="Options menu"] adjoining the listed release, and select *Rollback*.
1. In the *Rollback Helm Release* page, select the *Revision* you want to rollback to and click *Rollback*.
1. In the *Helm Releases* page, click on the chart to see the details and resources for that release.
1. Go to the *Revision History* tab to see all the revisions for the chart.
.Helm revision history
image::odc_helm_revision_history.png[]
1. If required, you can further use the Options menu image:kebab.png[title="Options menu"] adjoining a particular revision and select the revision to rollback to.
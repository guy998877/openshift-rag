# Watching for failed pods

To reduce troubleshooting time, regularly monitor for failed pods in your cluster.

.Procedure

- To watch for failed pods, run the following command:
```bash
$ oc get po -A | grep -Eiv 'complete|running'
```
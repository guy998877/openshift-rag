# Protocol for initiating port forwarding from a client

A client resource in your cluster can initiate port forwarding to a pod by issuing a request to the Kubernetes API server.

Use a request in the following format:

```bash
/proxy/nodes/<node_name>/portForward/<namespace>/<pod>
```
where:

--
`<node_name>`:: Specifies the FQDN of the node.
`<namespace>`:: Specifies the namespace of the target pod.
`<pod>`:: Specifies the name of the target pod.
--

.Example request
```bash
/proxy/nodes/node123.openshift.com/portForward/myns/mypod
```

After sending a port forward request to the API server, the client upgrades the
connection to one that supports multiplexed streams; the current implementation
uses [*Hyptertext Transfer Protocol Version 2 (HTTP/2)*](https://httpwg.org/specs/rfc7540.html).

The client creates a stream with the `port` header containing the target port in
the pod. All data written to the stream is delivered via the kubelet to the
target pod and port. Similarly, all data sent from the pod for that forwarded
connection is delivered back to the same stream in the client.

The client closes all streams, the upgraded connection, and the underlying
connection when it is finished with the port forwarding request.
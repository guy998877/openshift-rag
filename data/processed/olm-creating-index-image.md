# Creating a SQLite-based index image

You can create an index image based on the SQLite database format by using the `opm` CLI.

.Prerequisites

- You have installed the `opm` CLI.
- You have `podman` version 1.9.3+.
- A bundle image is built and pushed to a registry that supports link:https://docs.docker.com/registry/spec/manifest-v2-2/[Docker v2-2].

.Procedure

1. Start a new index:
```bash
$ opm index add \
    --bundles <registry>/<namespace>/<bundle_image_name>:<tag> \//<1>
    --tag <registry>/<namespace>/<index_image_name>:<tag> \//<2>
    [--binary-image <registry_base_image>] <3>
```
<1> Comma-separated list of bundle images to add to the index.
<2> The image tag that you want the index image to have.
<3> Optional: An alternative registry base image to use for serving the catalog.

1. Push the index image to a registry.

.. If required, authenticate with your target registry:
```bash
$ podman login <registry>
```

.. Push the index image:
```bash
$ podman push <registry>/<namespace>/<index_image_name>:<tag>
```
# Running image prune operations

Use the following procedure to run an image prune operation

.Prerequisites

- You must be logged into the CLI with an access token.
- You must have the `system:image-pruner` cluster role or greater (for example, `cluster-admin`).
- The image registry must be exposed.
- You have reviewed the "Considerations when manually pruning images" section of this document.

.Procedure

1. Optional: To preview which images would be pruned, enter the following command. This command prints a list of the images, image streams, and pods that would be removed. Note that nothing is deleted until you add the `--confirm` flag.
```bash
$ oc adm prune images <image_prune_option_one> <image_prune_option_two> <1>
```
<1> For more information about available pruning options, see "Manual image pruning command options".

1. Review the output to confirm the list of images, image streams, and pods to be removed.

1. Run the `oc adm prune images` command with the appropriate options for your cluster. Add the `--confirm` flag to confirm deletion. For example:
```bash
$ oc adm prune images <image_prune_option_one> <image_prune_option_two> --confirm
```
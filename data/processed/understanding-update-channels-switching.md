# Considerations for switching between channels

You can switch your cluster's update channel through the web console or the CLI, in order to access different update recommendations for your cluster.

You can switch the channel from the CLI by running the following command:

```bash
$ oc adm upgrade channel <channel>
```

The web console will display an alert if you switch to a channel that does not include the current release. The web console does not recommend any updates while on a channel without the current release. You can return to the original channel at any point, however.

Changing your channel might impact the supportability of your cluster. The following conditions might apply:

- Your cluster is still supported if you change from the `stable-4.21` channel to the `fast-4.21` channel.

- You can switch to the `candidate-4.21` channel at any time, but some releases for this channel might be unsupported.

- You can switch from the `candidate-4.21` channel to the `fast-4.21` channel if your current release is a general availability release.

- You can always switch from the `fast-4.21` channel to the `stable-4.21` channel. There is a possible delay of up to a day for the release to be promoted to `stable-4.21` if the current release was recently promoted.
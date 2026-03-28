# Using advanced Rsync features

You can use the additional command-line options that are available with the standard `rsync` command if needed. 

The `oc rsync` command exposes fewer command-line options than standard `rsync` command.
In the case that you want to use a standard `rsync` command-line option that is
not available with the `oc rsync` command, for example the `--exclude-from=FILE` option, it
might be possible to use standard `rsync` with the `--rsh` (`-e`) option or `RSYNC_RSH`
environment variable as a workaround, as shown in the following examples:

```bash
$ rsync --rsh='oc rsh' --exclude-from=<file_name> <local-dir> <pod-name>:/<remote-dir>
```

or:

Export the `RSYNC_RSH` variable:

```bash
$ export RSYNC_RSH='oc rsh'
```

Then, run the rsync command:

```bash
$ rsync --exclude-from=<file_name> <local-dir> <pod-name>:/<remote-dir>
```

Both of the above examples configure the standard `rsync` command to use `oc rsh` as its
remote shell program to enable it to connect to the remote pod, and are an
alternative to running `oc rsync`.
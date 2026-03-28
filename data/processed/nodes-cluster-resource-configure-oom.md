# Understanding OOM kill policy

OpenShift Container Platform can kill a process in a container if the total memory usage of all the processes in the container exceeds the memory limit, or in serious cases of node memory exhaustion.

If a process is Out of Memory (OOM) killed, the container could exit immediately. If the container PID 1 process receives the *SIGKILL*, the container does exit immediately. Otherwise, the container behavior is dependent on the behavior of the other processes.

For example, a container process exited with code 137, indicating it received a SIGKILL signal.

If the container does not exit immediately, use the following stepts to detect if an OOM kill occurred.

.Procedure

1. Access the pod using a remote shell:
```bash
# oc rsh <pod name>
```

1. Run the following command to see the current OOM kill count in `/sys/fs/cgroup/memory/memory.oom_control`:
```bash
$ grep '^oom_kill ' /sys/fs/cgroup/memory/memory.oom_control
```
.Example output
```bash
oom_kill 0
```

1. Run the following command to provoke an OOM kill:
```bash
$ sed -e '' </dev/zero
```
.Example output
```bash
Killed
```

1. Run the following command to see that the OOM kill counter in `/sys/fs/cgroup/memory/memory.oom_control` incremented:
```bash
$ grep '^oom_kill ' /sys/fs/cgroup/memory/memory.oom_control
```
.Example output
```bash
oom_kill 1
```
If one or more processes in a pod are OOM killed, when the pod subsequently exits, whether immediately or not, it will have phase *Failed* and reason *OOMKilled*. An OOM-killed pod might be restarted depending on the value of `restartPolicy`. If not restarted, controllers such as the replication controller will notice the pod's failed status and create a new pod to replace the old one.
Use the following command to get the pod status:
```bash
$ oc get pod test
```
.Example output
```bash
NAME      READY     STATUS      RESTARTS   AGE
test      0/1       OOMKilled   0          1m
```

- If the pod has not restarted, run the following command to view the pod:
```bash
$ oc get pod test -o yaml
```
.Example output
```bash
apiVersion: v1
kind: Pod
metadata:
  name: test
# ...
status:
  containerStatuses:
  - name: test
    ready: false
    restartCount: 0
    state:
      terminated:
        exitCode: 137
        reason: OOMKilled
  phase: Failed
```

- If restarted, run the following command to view the pod:
```bash
$ oc get pod test -o yaml
```
.Example output
```bash
apiVersion: v1
kind: Pod
metadata:
  name: test
# ...
status:
  containerStatuses:
  - name: test
    ready: true
    restartCount: 1
    lastState:
      terminated:
        exitCode: 137
        reason: OOMKilled
    state:
      running:
  phase: Running
```
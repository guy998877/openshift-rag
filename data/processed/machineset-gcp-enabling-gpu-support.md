# Enabling GPU support for a compute machine set

Use the Google Cloud Compute Engine to add GPUs to Virtual Machine (VM) instances. Workloads that benefit from access to GPU resources can perform better on compute machines with this feature enabled. OpenShift Container Platform on Google Cloud supports NVIDIA GPU models in the A2 and N1 machine series.

.Supported GPU configurations
|====
|Model name |GPU type |Machine types ^[1]^

|NVIDIA A100
|`nvidia-tesla-a100`
a|* `a2-highgpu-1g`
- `a2-highgpu-2g`
- `a2-highgpu-4g`
- `a2-highgpu-8g`
- `a2-megagpu-16g`

|NVIDIA K80
|`nvidia-tesla-k80`
.5+a|* `n1-standard-1`
- `n1-standard-2`
- `n1-standard-4`
- `n1-standard-8`
- `n1-standard-16`
- `n1-standard-32`
- `n1-standard-64`
- `n1-standard-96`
- `n1-highmem-2`
- `n1-highmem-4`
- `n1-highmem-8`
- `n1-highmem-16`
- `n1-highmem-32`
- `n1-highmem-64`
- `n1-highmem-96`
- `n1-highcpu-2`
- `n1-highcpu-4`
- `n1-highcpu-8`
- `n1-highcpu-16`
- `n1-highcpu-32`
- `n1-highcpu-64`
- `n1-highcpu-96`

|NVIDIA P100
|`nvidia-tesla-p100`

|NVIDIA P4
|`nvidia-tesla-p4`

|NVIDIA T4
|`nvidia-tesla-t4`

|NVIDIA V100
|`nvidia-tesla-v100`

|====
[.small]
--
1. For more information about machine types, including specifications, compatibility, regional availability, and limitations, see the Google Cloud Compute Engine documentation about [N1 machine series](https://cloud.google.com/compute/docs/general-purpose-machines#n1_machines), [A2 machine series](https://cloud.google.com/compute/docs/accelerator-optimized-machines#a2_vms), and [GPU regions and zones availability](https://cloud.google.com/compute/docs/gpus/gpu-regions-zones#gpu_regions_and_zones).
--

You can define which supported GPU to use for an instance by using the Machine API.

You can configure machines in the N1 machine series to deploy with one of the supported GPU types. Machines in the A2 machine series come with associated GPUs, and cannot use guest accelerators.

> **NOTE:** GPUs for graphics workloads are not supported.

.Procedure

1. In a text editor, open the YAML file for an existing compute machine set or create a new one.

1. Specify a GPU configuration under the `providerSpec` field in your compute machine set YAML file. See the following examples of valid configurations:
.Example configuration for the A2 machine series
```yaml
  providerSpec:
    value:
      machineType: a2-highgpu-1g
      onHostMaintenance: Terminate
      restartPolicy: Always
```
where
--
`spec.template.spec.providerSpec.value.machineType`:: Specifies the machine type. Ensure that the machine type is included in the A2 machine series.
`spec.template.spec.providerSpec.value.onHostMaintenance`:: Sets `onHostMaintenance` to `Terminate`. When using GPU support, you must set `onHostMaintenance` to `Terminate`.
`spec.template.spec.providerSpec.value.restartPolicy`:: Specifies the restart policy for machines deployed by the compute machine set. The allowed values are `Always` or `Never`.
--
.Example configuration for the N1 machine series
```yaml
providerSpec:
  value:
    gpus:
    - count: 1
      type: nvidia-tesla-p100
    machineType: n1-standard-1
    onHostMaintenance: Terminate
    restartPolicy: Always
```
where
--
`spec.template.spec.providerSpec.value.gpus.count`:: Specifies the number of GPUs to attach to the machine.
`spec.template.spec.providerSpec.value.gpus.type`:: Specifies the type of GPUs to attach to the machine. Ensure that the machine type and GPU type are compatible.
`spec.template.spec.providerSpec.value.machineType`:: Specifies the machine type. Ensure that the machine type and GPU type are compatible.
`spec.template.spec.providerSpec.value.onHostMaintenance`:: Sets `onHostMaintenance` to `Terminate`. When using GPU support, you must set `onHostMaintenance` to `Terminate`.
`spec.template.spec.providerSpec.value.restartPolicy`:: Specifies the restart policy for machines deployed by the compute machine set. The allowed values are `Always` or `Never`.
--
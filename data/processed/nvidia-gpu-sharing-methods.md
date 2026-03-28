# GPU sharing methods

Red Hat and NVIDIA have developed GPU concurrency and sharing mechanisms to simplify GPU-accelerated computing on an enterprise-level OpenShift Container Platform cluster.

Applications typically have different compute requirements that can leave GPUs underutilized. Providing the right amount of compute resources for each workload is critical to reduce deployment cost and maximize GPU utilization.

Concurrency mechanisms for improving GPU utilization exist that range from programming model APIs to system software and hardware partitioning, including virtualization. The following list shows the GPU concurrency mechanisms:

- Compute Unified Device Architecture (CUDA) streams
- Time-slicing
- CUDA Multi-Process Service (MPS)
- Multi-instance GPU (MIG)
- Virtualization with vGPU

Consider the following GPU sharing suggestions when using the GPU concurrency mechanisms for different OpenShift Container Platform scenarios:

Bare metal:: vGPU is not available. Consider using MIG-enabled cards.
VMs:: vGPU is the best choice.
Older NVIDIA cards with no MIG on bare metal:: Consider using time-slicing.
VMs with multiple GPUs and you want passthrough and vGPU:: Consider using separate VMs.
Bare metal with OpenShift Virtualization and multiple GPUs:: Consider using pass-through for hosted VMs and time-slicing for containers.
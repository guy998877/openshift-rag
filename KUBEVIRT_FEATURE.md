# KubeVirt Feature Branch

## Overview

This branch explores running legacy workload VMs (like asciidoctor converters) alongside Kubernetes containers using KubeVirt.

## What's Included

**Kubernetes Manifests** (`k8s/kubevirt/`):
- `vm-asciidoc-converter.yaml` — KubeVirt VirtualMachine running Fedora 40 with asciidoctor and Python HTTP server on port 8080
- `vm-service.yaml` — ClusterIP Service for VM access

**Key Concept**:
Instead of containerizing every workload, KubeVirt allows running VMs as first-class Kubernetes objects. This is useful for:
- Legacy applications that require full OS access
- Complex setup that's harder to containerize
- Gradual migration from VM-based to container-based infrastructure

## Limitations

- Requires KVM hardware support (`/dev/kvm`) — not available in macOS Docker
- VMs consume more resources than containers
- Additional networking complexity vs. pure container approach

## Testing

Created VM manifests but unable to boot on macOS (expected — KVM support limited to Linux hosts).

---

For production use, consider containerizing new services instead of running VMs in Kubernetes.

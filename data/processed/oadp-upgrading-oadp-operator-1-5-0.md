# Upgrading the OADP Operator

You can upgrade the OpenShift API for Data Protection (OADP) Operator using the following procedure. 

> **NOTE:** Do not install OADP 1.5.0 on a {OCP-short} 4.18 cluster.

.Prerequisites

- You have installed the latest OADP 1.4.6.
- You have backed up your data.

.Procedure

1. Upgrade {OCP-short} 4.18 to {OCP-short} 4.19.
> **NOTE:** OpenShift API for Data Protection (OADP) 1.4 is not supported on {OCP-short} 4.19.
1. Change your subscription channel for the OADP Operator from `stable-1.4` to `stable`.
1. Wait for the Operator and containers to update and restart.
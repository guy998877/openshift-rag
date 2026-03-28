ifdef::aws[= Creating Spot Instances by using compute machine sets]
ifdef::azure[= Creating Spot VMs by using compute machine sets]
ifdef::gcp[= Creating Spot VMs by using compute machine sets]
ifdef::gcp-legacy-preempt[= Creating preemptible VM instances by using compute machine sets]

You can save on costs by creating a compute machine set that deploys machines as non-guaranteed instances.
ifdef::aws[To launch a Spot Instance on AWS, you add `spotMarketOptions` to your compute machine set YAML file.]
ifdef::azure[To launch a Spot VM on Azure, you add `spotVMOptions` to your compute machine set YAML file.]
ifdef::gcp[To launch a Spot VM on Google Cloud, you add `provisioningModel: "Spot"` to your compute machine set YAML file.]

.Procedure
- Add the following line under the `providerSpec` field:
# Submitting a support case

Submit a support case to Red Hat Support to get help with issues you encounter with OpenShift Container Platform.

.Prerequisites

- You have access to the cluster as a user with the `cluster-admin` role.
- You have installed the OpenShift CLI (`oc`).
- You have a Red Hat Customer Portal account.
- You have a Red Hat Standard or Premium subscription.

.Procedure

1. Log in to link:https://access.redhat.com/support/cases/#/case/list[the *Customer Support* page] of the Red Hat Customer Portal.

1. Click *Get support*.

1. On the *Cases* tab of the *Customer Support* page:

.. Optional: Change the pre-filled account and owner details if needed.

.. Select the appropriate category for your issue, such as *Bug or Defect*, and click *Continue*.

1. Enter the following information:

.. In the *Summary* field, enter a concise but descriptive problem summary and further details about the symptoms being experienced, as well as your expectations.

.. Select *OpenShift Container Platform* from the *Product* drop-down menu.

.. Select *4.21* from the *Version* drop-down.

1. Review the list of suggested Red Hat Knowledgebase solutions for a potential match against the problem that is being reported. If the suggested articles do not address the issue, click *Continue*.

1. Review the updated list of suggested Red Hat Knowledgebase solutions for a potential match against the problem that is being reported. The list is refined as you provide more information during the case creation process. If the suggested articles do not address the issue, click *Continue*.

1. Ensure that the account information presented is as expected, and if not, amend accordingly.

1. Check that the autofilled OpenShift Container Platform Cluster ID is correct. If it is not, manually obtain your cluster ID.
- To manually obtain your cluster ID using the OpenShift Container Platform web console:
.. Navigate to *Home* -> *Overview*.
.. Find the value in the *Cluster ID* field of the *Details* section.
- Alternatively, it is possible to open a new support case through the OpenShift Container Platform web console and have your cluster ID autofilled.
.. From the toolbar, navigate to *(?) Help* -> *Open Support Case*.
.. The *Cluster ID* value is autofilled.
- To obtain your cluster ID using the OpenShift CLI (`oc`), run the following command:
```bash
$ oc get clusterversion -o jsonpath='{.items[].spec.clusterID}{"\n"}'
```

1. Complete the following questions where prompted and then click *Continue*:
- What are you experiencing? What are you expecting to happen?
- Define the value or impact to you or the business.
- Where are you experiencing this behavior? What environment?
- When does this behavior occur? Frequency? Repeatedly? At certain times?

1. Upload relevant diagnostic data files and click *Continue*.
It is recommended to include data gathered using the `oc adm must-gather` command as a starting point, plus any issue specific data that is not collected by that command.

1. Input relevant case management details and click *Continue*.

1. Preview the case details and click *Submit*.
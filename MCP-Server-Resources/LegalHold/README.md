# Legal Hold Agent Resources

These resources configure the behavior of the Legal Hold Agent, specifying hold naming conventions, class-to-hold mappings, and release conditions.

## Files

| File | Type | What it does | Tested Resource Description |
|---|---|---|---|
| [`LH_template.json`](LH_template.json) | Template (Customize & Upload) | Defines hold naming rules, document class-to-hold mappings, relevancy guidelines, and hold release metadata conditions. | `Always read this resource before responding to any hold request. Required before asking clarifying questions or taking any action, including releasing from hold. This resource contains the class-to-hold mapping, hold naming rules, relevancy assessment guidance, and release conditions.` |

## Examples

> [!WARNING]
> These example files are designed for reference and illustration. They require modification prior to use to match your organization's specific Content Platform Engine class symbolic names, custom metadata properties, and regulatory rules.

The [`examples/`](examples) directory contains Reference Examples (Analyze & Adapt) for different business verticals:

* [`LH_healthcare_hold_policy.json`](examples/LH_healthcare_hold_policy.json)
  * A healthcare-aligned policy mapping patient records (`PATIENT_{PatientMRN}`) and validating clinical malpractice dispute properties prior to releasing holds.
* [`LH_gov_hold_policy.json`](examples/LH_gov_hold_policy.json)
  * A public sector policy supporting FOIA case-based holds (`FOIA_{RequestTrackingNumber}`) and validating appeal/adjudication statuses prior to releasing holds.
* [`LH_financial_hold_policy.json`](examples/LH_financial_hold_policy.json)
  * An FSI policy supporting loan and claim holds (`LOAN_{LoanNumber}`) and validating loan payment or claim settlement properties prior to releasing holds.

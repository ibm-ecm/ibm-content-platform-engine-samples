# Redaction Agent Resources

These resources configure the behavior of the Redaction Agent, specifying document output behaviors, save modes, and sensitive content categories.

## Files

| File | Type | What it does | Tested Resource Description |
|---|---|---|---|
| [`RD_policy_template.json`](RD_policy_template.json) | Template (Customize & Upload) | Controls output format defaults (PDF/TIFF), save modes (new document or version), and deployment-level sensitivity configuration. | `Always read this resource before responding to any redaction request. Required before asking clarifying questions or taking any action. This resource contains output format defaults, class-based output rules, and sensitivity configuration.` |
| [`RD_patterns_template.json`](RD_patterns_template.json) | Template (Customize & Upload) | Defines sensitive content categories (e.g. account numbers, names) to look for and redact for a specific business domain. | `Always read this resource before responding to any redaction request involving [domain type]. Required before asking clarifying questions or taking any action. This resource contains the sensitive content categories to identify and redact for this domain.` (Replace `[domain type]` with yours). |

## Examples

> [!WARNING]
> These example files are designed for reference and illustration. They require modification prior to use to match your organization's specific Content Platform Engine class symbolic names, custom metadata properties, and regulatory rules.

The [`examples/`](examples) directory contains Reference Examples (Analyze & Adapt):

* [`RD_policy_healthcare.json`](examples/RD_policy_healthcare.json)
  * A HIPAA-aligned policy mapping clinical files to `new_document` releases while maintaining billing records as `new_version` updates in place. Protects personal clinical identifiers while ensuring treating facilities and doctor names stay intact.
* [`RD_policy_gov.json`](examples/RD_policy_gov.json)
  * A public sector policy that preserves contract award amounts and agency names for civic transparency, while redacting law enforcement informants, juvenile records, and private tax IDs.
* [`RD_policy_financial.json`](examples/RD_policy_financial.json)
  * A GLBA and PCI-DSS-aligned policy that always redacts credit card primary account numbers (PAN), CVVs, and tax forms, while preserving interest rates and approved loan amounts.

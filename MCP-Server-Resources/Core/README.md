# Core Agent Resources

These resources configure the behavior of the Core Agent for document classification, search settings, and text extraction rules.

## Files

| File | Type | What it does | Tested Resource Description |
|---|---|---|---|
| [`classification_policy_template.json`](classification_policy_template.json) | Template (Customize & Upload) | Defines classification rules, confidence thresholds, target classes, and locked classes. | `Always use this resource when performing initial classification of unclassified documents or for any reclassification request. Required before asking clarifying questions or taking any action. This resource contains eligible source classes, target classes, locked classes, confidence thresholds, and fallback rules.` |
| [`smart_search_settings.json`](smart_search_settings.json) | Drop-and-Use (Direct Upload) | Reorders vector search execution, forcing metadata filtering to apply on top of vector results. | `REQUIRED: Do not call smart_document_search until you have read this resource in the current request. Contains mandatory parameter rules that must be applied to every search call.` |
| [`text_extract_settings.json`](text_extract_settings.json) | Drop-and-Use (Direct Upload) | Controls text extraction outputs (e.g. returning plain text, key-value pairs, and tables instead of raw markdown output). | `REQUIRED: Do not call get_document_text_extract until you have read this resource in the current request. Contains mandatory parameter rules that must be applied to every text extract call.` |

## Examples

> [!WARNING]
> These example files are designed for reference and illustration. They require modification prior to use to match your organization's specific Content Platform Engine class symbolic names, custom metadata properties, and regulatory rules.

The [`examples/`](examples) directory contains Reference Examples (Analyze & Adapt) tailored to specific business domains:

* [`healthcare_classification_policy.json`](examples/healthcare_classification_policy.json)
  * A HIPAA-aligned clinical policy with high confidence requirements (`0.85`/`0.90`) and strict clinician signature validation checks to prevent unauthorized reclassifications.
* [`gov_classification_policy.json`](examples/gov_classification_policy.json)
  * A public sector archival and FOIA-aligned policy with standardized archiving checks (`0.80`/`0.85`) and locks to preserve record accountability.
* [`financial_classification_policy.json`](examples/financial_classification_policy.json)
  * A GLBA and SOX-aligned financial policy with stringent thresholds (`0.88`/`0.92`) and locks protecting closed or disbursed loan/debt records.

# Content Cortex MCP Server Resource samples

Out-of-the-box templates, settings files, and domain policy examples for Content Cortex AI agents. These resources serve two purposes: they define the rules and policies that guide agent behavior (output formats, hold naming conventions, permitted tools), and they ground the agent in your organization's specific content model, including your document classes, custom properties, and metadata structure. Together they allow agents to intelligently navigate and act on your enterprise content.

## Resource Types

To make adoption as easy as possible, our resources are categorized into three types:

* **Templates (Customize & Upload):** Empty frameworks with placeholder values. Fill in your organization's document class names, properties, and rules, then upload.
* **Drop-and-Use (Direct Upload):** Pre-configured, tested settings files that can be uploaded directly with **no modifications** to enforce specific agent parameters.
* **Reference Examples (Analyze & Adapt):** Fully completed policies for specific industries (Healthcare, Government, Financial Services). These are not for direct upload as class names and properties will not match your object store. Use them to understand what a finished policy looks like before building your own from a template.

## Folders

The resources are organized by agent type:

* [**Core Agent**](./Core/)
  * Guides document classification, reclassification, smart document search, and text extraction settings.
* [**Legal Hold Agent**](./LegalHold/)
  * Controls legal hold naming, class-to-hold mappings, relevancy checks, and hold release conditions.
* [**Redaction Agent**](./Redaction/)
  * Manages redaction output formats (PDF/TIFF), save modes (new document or version), and regulatory sensitivity rules.

Refer to the `README.md` inside each folder for a detailed description of its files and guidance on how to adopt them.

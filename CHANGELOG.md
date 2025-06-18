# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]


## [5.7.0.0] - 2025-06-20

### Added
- Added [.secrets.baseline](.secrets.baseline) for detect-secrets
- Added missing deploy_select_cd.ipynb
- Added [gqlinvoke_content_assistant_samples.ipynb](CS-Deployment-API/gqlinvoke_content_assistant_samples.ipynb).
- Added [WAS CPE Must Gather Scripts](MustGather).

### Changed
- Updated [ClamAV.zip](ClamAVContentValidator/files/ClamAV.zip) in the [Content Validation with ClamAV sample application project](ClamAVContentValidator) to fix an inconsistency in the `Main-Class` attribute for the MANIFEST.MF file in ClamAV.jar.
- Updated [deploy_select_cd.ipynb](CS-Deployment-API/deploy_select_cd.ipynb) to remove default ssl_enabled flag in basic target_connection.
- Updated [README.md] to add potential ways to launch notebook for Windows OS via command line.

### Removed
- Removed the **Content Services on Amazon Web Services sample applications**.
  - These code samples were specific to the Content Services on Amazon Web Services offering, which has since been discontinued. For sample code on how to use the Content Engine client API to authenticate with an OAuth token, see [Single sign-on integrations via Content Engine API Bearer Token Authentication](https://www.ibm.com/docs/en/filenet-p8-platform/5.6.0?topic=authentication-single-sign-integrations-via-content-engine-api-bearer-token).


## [5.6.0.0] - 2024-06-28

### Added
- Added the [Content Validation with ClamAV sample application project](ClamAVContentValidator).
- Added the [Content Services GraphQL API Schema project](CS-GraphQL-Schema) with the schema for FNCM 5.6.0.

### Changed
- Updated [Content Services GraphQL API Javascript Sample Application](CS-GraphQL-javascript-samples) to add upload document with streaming.
- Renamed the [Content Services Metadata Deployment Sample Application project](CS-MetadataDeployment) to the [Content Services Deployment API project](CS-Deployment-API).
- Moved Jupyter notebooks of the old project from the folder [CS-MetadataDeployment](CS-MetadataDeployment) to the folder [CS-Deployment-API](CS-Deployment-API).
- Removed the old [Deployment API samples](CS-MetadataDeployment). Users can now use the new Content Services Deployment API package included in FNCM 5.6.0 installation media instead of the old sample project.
- Updated the project to use the new CS GraphQL APIs from FNCM 5.6.0 and reorganized the Jupyter notebooks.
- Updated copyright date to 2024.
- Updated [LICENSE](LICENSE) to IBM FileNet Content Manager v5.6.0.


## [5.5.12.0] - 2023-12-15

### Added
- Added the [Content Services on Amazon Web Services sample applications](CSAWS), including the
  following [sub-projects for working with API keys/APIC tokens](CSAWS/API-key):
  - [CE .NET API code sample using OAUTH authentication via APIC CEWS endpoint](CSAWS/API-key/CE-dotNET-API-key)
  - [Content Engine Java API sample application for API keys in a Content Services on AWS environment](CSAWS/API-key/cejavaapikey)
  - [GraphQL client using API key Java sample application](CSAWS/API-key/CS-GraphQL-API-key-Java)
  - [GraphQL client using API key Python sample application](CSAWS/API-key/CS-GraphQL-API-key-Python)
- Added the [**Content Services Metadata Deployment Sample Application**](CS-MetadataDeployment).

### Changed
- Updated [LICENSE](LICENSE) to IBM FileNet Content Manager v5.5.12.


## [5.5.11.0] - 2023-06-23

### Added
- Added the [Content Services GraphQL API Javascript Sample Application project](CS-GraphQL-javascript-samples).

### Changed
- Updated [LICENSE](LICENSE) to IBM FileNet Content Manager v5.5.11.


## [5.5.8.0] - 2021-12-16

### Changed
- Updated the [scripts](CSGraphQLAPIDeployScripts) to deploy the Content Services GraphQL API
  application on a traditional WebSphere Application Server.
  - Changed GraphQL application name to be a parameter
  - Changed suggest folder paths in sample properties file
  - Added changes to support deploying GraphQL application in the same
    WAS profile as CPE
  - Renamed "CPE Client Libs" shared library to remove CPE version number


## [5.5.7.0] - 2021-06-25

### Added
- Added the [Content Services GraphQL API Deploy Scripts project](CSGraphQLAPIDeployScripts).

### Changed
- Updated [README.md](ContentEventWebhookReceiver/README.md).
- Changed Javadoc, expanding instances of "CPE" to "Content Platform Engine."
- Replaced JCenter repository with Maven Central in the Webhook Receiver sample application.


## [5.5.4.0] - 2019-12-12

### Added
- Created the IBM Content Platform Engine samples repository.
- Added initial version of all files and folders to the root of the repository.
- Added the [Content Event Webhook Receiver sample application project](ContentEventWebhookReceiver)
- Added [Javadoc](https://ibm-ecm.github.io/ibm-content-platform-engine-samples/ContentEventWebhookReceiver/) for the Content Event Webhook Receiver sample application project to the [docs](docs) folder
- Enabled [Github Pages](https://pages.github.com/) on the samples repository.

[unreleased]: https://github.com/ibm-ecm/ibm-content-platform-engine-samples/compare/v5.7.0.0...HEAD
[5.7.0.0]: https://github.com/ibm-ecm/ibm-content-platform-engine-samples/releases/tag/v5.7.0.0
[5.6.0.0]: https://github.com/ibm-ecm/ibm-content-platform-engine-samples/releases/tag/v5.6.0.0
[5.5.12.0]: https://github.com/ibm-ecm/ibm-content-platform-engine-samples/releases/tag/v5.5.12.0
[5.5.11.0]: https://github.com/ibm-ecm/ibm-content-platform-engine-samples/releases/tag/v5.5.11.0
[5.5.8.0]: https://github.com/ibm-ecm/ibm-content-platform-engine-samples/releases/tag/v5.5.8.0
[5.5.7.0]: https://github.com/ibm-ecm/ibm-content-platform-engine-samples/releases/tag/v5.5.7.0
[5.5.4.0]: https://github.com/ibm-ecm/ibm-content-platform-engine-samples/releases/tag/v5.5.4.0

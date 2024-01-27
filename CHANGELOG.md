# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased] - 2024-01-26

### Added
- Added the [Content Validation with ClamAV sample application project](ClamAVContentValidator).

### Changed
- Updated [Content Services GraphQL API Javascript Sample Application](CS-GraphQL-javascript-samples) to add upload document with streaming.
- Updated copyright date to 2024.


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

[unreleased]: https://github.com/ibm-ecm/ibm-content-platform-engine-samples/compare/v5.5.12.0...HEAD
[5.5.12.0]: https://github.com/ibm-ecm/ibm-content-platform-engine-samples/releases/tag/v5.5.12.0
[5.5.11.0]: https://github.com/ibm-ecm/ibm-content-platform-engine-samples/releases/tag/v5.5.11.0
[5.5.8.0]: https://github.com/ibm-ecm/ibm-content-platform-engine-samples/releases/tag/v5.5.8.0
[5.5.7.0]: https://github.com/ibm-ecm/ibm-content-platform-engine-samples/releases/tag/v5.5.7.0
[5.5.4.0]: https://github.com/ibm-ecm/ibm-content-platform-engine-samples/releases/tag/v5.5.4.0

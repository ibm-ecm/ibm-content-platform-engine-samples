# Content Validation sample code

The CPE 5.5.12 release includes a preview of a new feature called Content Validation. This feature allows a custom plugin executing in the server to inspect content as it is uploaded and reject that which is deemed inappropriate, for example if it contains executable code or a virus.

As part of the preview a sample content validator is being provided which submits the content to a ClamAV virus detection daemon service.

### Contents of this sample component
This sample contains the following:

- The source for the sample handler [ClamAVContentValidator.java](src/ClamAVContentValidator.java).
- A document describing how to configure the handler [ClamAVConfig.pdf](doc/ClamAVConfig.pdf).
- A zip file [ClamAV.zip](files/ClamAV.zip) containing the above two files plus the built code in jar form.


# csdeploy-python-sample
# Introduction
This sample demonstrates using Python to invoke Content Services GraphQL API to deploy of metadata such as Property Templates, Choices Lists, and Class Definitions across Content Platform Engine (CPE) Object Stores (OS) – export from source CPE domain/OS then import into target CPE domain/OS.
Features demonstrated in the sample:
- Export Class Definition(s) and dependencies like Property Template(s) and Choice List(s) for subclasses of system classes such as - Document, Folder, CustomObject, CmAbstractPersistable and Annotation.
- Discover whether dependencies of an exported Class Definition exist in the target import object store.
- Import, create and/or update, Class Definition(s) and dependencies.
# Usage
The sample includes two Jupyter notebooks: <br>
- **demo.ipynb** - Simple walkthrough of export and import
- **demo_api.ipynb** - Detailed walkthrough of export and import, grouping functions into Python packages/functions


# Python Installation
**Windows:**
1. Download Python from the official website: https://www.python.org/downloads/
2. Run the installer.
3. During installation, make sure to check the box that says "Add Python x.x to PATH" (where x.x is the version number).
4. Complete the installation process.

**macOS and Linux:**
1. Download Python from the official website: https://www.python.org/downloads/macos/
2. Run the installer.
3. Complete the installation process.
4. A Finder window should pop up containing the file "Update Shell Profile.command". Run this file. If this finder window did not pop up, navigate to Applications and look for the python folder. The command file should be in here.

# Prerequisite
- Functional Python3 instance, downloadable from: https://www.python.org/downloads/
- Functional Jupyter library: `python3 -m pip install jupyter`
- Python Requests library:
`python3 -m pip install requests` 

# Instruction
Before using this program, make sure to edit ``config.py`` to match with the intended endpoints and authentication mechanism.

To launch the demo notebook, you can do the following:<br>
- Call demo.ipynb as a jupyter lab launch: 
`jupyter ./demo.ipynb`
- Launch startup.sh: `./startup.sh` or double click the script

To launch the demo_api notebook, you can do the following:
- Call demo.ipynb as a jupyter lab launch: 
`jupyter ./demo_api.ipynb`

# Limitation
This is a sample only and as such there are several limitations. Some of these limitations are:
- The system classes themselves are not exported nor imported. For example if property definitions were added to the base Document class, those property definitions would not be imported into a target system.
- Metadata that is installed by an add-on is not recognized as such. For example if a sub-class of Document was created by an add-on in the source system and then exported by this sample tool. Note that this exporting could be the result of being a dependency on some other class. It may be exported and imported successfully but there will be no record in the target system that the sub-class was installed by an add-on. The add-on instead should be used to import this metadata into the target system.
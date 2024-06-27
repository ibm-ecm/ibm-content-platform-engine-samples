# CS-Deployment-API
# Introduction
This sample demonstrates the usage of Content Services Deployment Python API to invoke Content Services GraphQL API to deploy of metadata such as Property Templates, Choice Lists, and Class Definitions across Content Platform Engine (CPE) Object Stores (OS) – export from source CPE domain/OS then import into destination CPE domain/OS.
# Features in Sample Notebooks:
- Export Class Definition(s) and dependencies like Property Template(s) and Choice List(s) for subclasses of system classes such as - Document, Folder, CustomObject, CmAbstractPersistable and Annotation.
- Export all objects of any or all types in Class Definition(s), Property Template(s) and Choice List(s).
- Usage of Import Options - selecting to only import if the object is newer on the source OS than it is on destination OS.
- Import, create and/or update, Class Definition(s), Property Template(s), and Choice List(s) and their dependencies.
# Usage
The sample includes three Jupyter notebooks: <br>
- **deploy_select_cd.ipynb** - Export and import select class definition.
- **deploy_all_cd.ipynb** - Export and import all class definitions. Additionally demonstrates audit logger for API audit operations.
- **deploy_all.ipynb** - Export and import all class definitions, property templates, choice lists modified after a given date and their dependencies. Additionally demonstrates audit logger usage and import options.

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
- Functional Jupyter library: `python3 -m pip install jupyter` or `python -m pip install jupyter`
- Installed CSDeploy whl distribution package:
`python3 -m pip install <PATH_TO_WHL>` or `python -m pip install <PATH_TO_WHL>`

# Instruction
Before using this program, make sure to edit ``config.py`` to match with the intended endpoints and authentication mechanism.

To launch any of the demo notebook, you can do the following from directory containing notebooks:<br>
- Call deploy_select_cd.ipynb as a jupyter lab launch: <br>
`jupyter ./deploy_select_cd.ipynb` or `python3 -m jupyter ./deploy_select_cd.ipynb` or `python -m jupyter ./deploy_select_cd.ipynb`
- Call deploy_all_cd.ipynb as a jupyter lab launch: <br>
`jupyter ./deploy_all_cd.ipynb` or `python3 -m jupyter ./deploy_all_cd.ipynb` or `python -m jupyter ./deploy_all_cd.ipynb`
- Call deploy_all.ipynb as a jupyter lab launch: <br>
`jupyter ./deploy_all.ipynb` or `python3 -m jupyter ./deploy_all.ipynb` or `python -m jupyter ./deploy_all.ipynb`
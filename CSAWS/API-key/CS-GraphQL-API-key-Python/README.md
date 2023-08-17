# Usage
This program demonstrates simple implementations of a GraphQL program by leveraging AWS GraphQL's API.

# Python Installation
**Windows:**
1. Download Python from the official website: https://www.python.org/downloads/
2. Run the installer.
3. During installation, make sure to check the box that says "Add Python x.x to PATH" (where x.x is the version number).
4. Complete the installation process.

**macOS and Linux:**
1. Python is usually pre-installed on macOS and many Linux distributions. Open a terminal and check if Python is already installed by typing 
   - `python3 --version`.
2. If Python is not installed, you can install it using your system's package manager. For example, on Ubuntu, you can use:
   - `sudo apt update`
   - `sudo apt install python3`
3. After installing Python, open a terminal and enter the following command to find the Python installation path:
   `which python3`
  
4. Copy the path that is displayed.
5. Run following line, replacing `/path/to/python` with the actual path you copied in step 4:
   - `echo export PATH="</path/to/python>:$PATH" >> ~/.bash_profile`
6. Save the file and exit the text editor.
7. To apply the changes, either restart your terminal or run the following command:
   - `source ~/.bash_profile`
8. Test if Python is added to the PATH by typing `python3 --version` in the terminal.
Please note that the exact steps might vary slightly depending on your specific operating system version and configuration. If you encounter any issues or need further assistance, feel free to ask! 

# Prerequisite
- Functional Python3 instance, downloadable from: https://www.python.org/downloads/
- Python Requests library:
`python3 -m pip install requests`

# Instruction
Before using this program, make sure to edit config.py to match with the intended endpoints.

Template of Variables:
- GQL_URL = `https://api-9o4.us-east-a.apiconnect.ibmappdomain.cloud/ibmcontentservices/csprod/${InstanceName}/content-services-graphql/graphql`
- APIC_TOKEN_URL =  `https://api-9o4.us-east-a.apiconnect.ibmappdomain.cloud/ibmcontentservices/csprod/${InstanceName}/token`
- SERVICE_USER_ID = `USERNAME@INSTANCENAME.fid`
- FILE_PATH = '/a/b/c'

Sample:
- GQL_URL = 'https://api-9o4.us-east-a.apiconnect.ibmappdomain.cloud/ibmcontentservices/csprod/gqlsample/content-services-graphql/graphql'
- APIC_TOKEN_URL =  'https://api-9o4.us-east-a.apiconnect.ibmappdomain.cloud/ibmcontentservices/csprod/gqlsample/token'
- SERVICE_USER_ID = 'TestUser@gqlsample.fid'
- SERVICE_USER_API_KEY = 'AA1bc2d%y*' 
- FILE_PATH = '/Users/test/Data'

To launch the program, call sample.py as a python program then follow the prompts.

`Python3 sample.py`

# Notes
For api generation usage, large numbers can cause a exponentially large amount of requests to be made to the graphql endpoint.



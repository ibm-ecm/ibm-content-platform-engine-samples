# WAS CPE Must Gather

# Introduction

This folder contains scripts to help collect logs and other necessary debugging information from people using the WebSphere installation of FileNet Content Manager.

There are two different scripts, one for Windows called `windows-script.ps1` written in PowerShell, and one for Linux called `linux-script.sh` written in bash.

Both use the configuration file `config`, which will be created if it does not exist.

> [!IMPORTANT]
> Make sure the user running the script has read access to the WebSphere files and write access to the output directory.

# Features
The following logs are collected:
- Ping Page (`index.html`)
- Ping Page Information
    - JDBC Driver (`JDBC_Driver.txt`)
    - Build Version (`Build_Version.txt`)
    - P8 Domain (`P8_Domain.txt`)
    - Server Instances (`Server_Instances.txt`)
- Java Version (`Java_Version.txt`)
- Logs from each server
    - `ce_trace`, `ce_system`, `pe_trace`, `pe_system`, and `SystemOut` logs for each server
    - `ffdc` logs

# Usage

Both the Linux and Windows scripts use the same formatting.

## Collecting Logs

```
./linux-script.sh
```
```
.\windows-script.ps1
```

When running these scripts, if the `config` file is not populated, the scripts will query the user for information to populate the `config` file.
On subsequent runs where the `config` file is filled, the scripts will not prompt the user, allowing for the logs to be collected automatically.

## Interactive Mode

If you wish to reconfigure the config file, you can either directly edit the `config` file or run the scripts with the `-i` flag.
This flag can be combined with any other keywords mentioned below, which will then prompt the user for any necessary config values needed to run.
```
./linux-script.sh -i
```
```
.\windows-script.ps1 -i
```
This will cause the script to prompt the user and repopulate the `config` file.

## Cleaning Logs

To clean the logs, you can run the scripts with the keyword `clean` passed into the script.

```
./linux-script.sh clean
```
```
.\windows-script.ps1 clean
```

## Help

To display a help message, you can run the scripts with the keyword `help` passed into the script.
```
./linux-script.sh help
```
```
.\windows-script.ps1 help
```

## Config File Options
- `WAS_ROOT_DIR`: The WebSphere root directory (e.g. `/opt/IBM/WebSphere/AppServer`).
- `OUTPUT_DIR`: The directory that the logs should be written to.
- `OVERWRITE`: Whether or not the files should have a timestamp appended to their name.
- `URL`: The url of the WebSphere ping page.
- `VERBOSE`: Whether or not to have the script output debug information.

# Output
The resulting logs are stored as a compressed file (`.tar.gz` or `.zip`), which can be sent for debugging purposes.

# Issues

## `curl` not installed
If your Windows or Linux installation does not come with `curl`, the script will output an error.
In this case, please follow these steps:

1. Go to your FileNet ping page on a web browser.
2. Right click the webpage and click "Save As."
3. Save the resulting HTML file to the output directory.
4. Recompress the output directory with the new files.
# Parameters: Takes in an optional flag -i and an optional action
param (
	[Parameter(HelpMessage = "Interactive mode")]
	[switch]$i = $false,
	[string]$action
)


# Remove need to verify certificates
[System.Net.ServicePointManager]::ServerCertificateValidationCallback = { $true }

# Config file to be read from.
$CONFIG_FILE = ".\config"

$config = @{
	"WAS_ROOT_DIR" = ""
	"URL"          = ""
	"OUTPUT_DIR"   = ""
	"VERBOSE"      = ""
	"OVERWRITE"    = ""
}

# Read values from config file
if (-not (Test-Path $CONFIG_FILE)) {
	New-Item -ItemType File -Name $CONFIG_FILE | Out-Null
}

Get-Content $CONFIG_FILE | ForEach-Object {
	if ($_ -like "*=*") {
		$var = ($_.split("="))[0]
		$config[$var] = ($_.split("="))[1]
	}
}

# Prompt the user for the WebSphere directory
function prompt_was_root() {
	while ($config["WAS_ROOT_DIR"] -eq "") {
		if ($Env:WAS_HOME -eq "" -or $null -eq $Env:WAS_HOME) {
			$ans = Read-Host "Please input the WebSphere Directory"
		}
		else {
			$ans = Read-Host "Please input the WebSphere Directory (default: ${Env:WAS_HOME})"
			
			if ($ans -eq "") {
				$ans = $Env:WAS_HOME
			}
		}
		
		if (-not (Test-Path $ans)) {
			Write-Host "This location does not exist. Please try again.\n"
			continue
		}
		
		$config["WAS_ROOT_DIR"] = $ans
		
		# Add the response to the config file
		if (Select-String -Path $CONFIG_FILE -Pattern "WAS_ROOT_DIR=" -Quiet) {
			(Get-Content $CONFIG_FILE) -replace ".*WAS_ROOT_DIR=.*", "WAS_ROOT_DIR=$($config['WAS_ROOT_DIR'])" | Set-Content $CONFIG_FILE
		}
		else {
			Add-Content -Path $CONFIG_FILE -Value "WAS_ROOT_DIR=$($config['WAS_ROOT_DIR'])"
		}
	}
}

# Prompt the user for the output directory
function prompt_output() {
	while ($config["OUTPUT_DIR"] -eq "") {
		$ans = Read-Host "Please input the output directory"
		
		$config["OUTPUT_DIR"] = $ans
		
		# Add the response to the config file
		if (Select-String -Path $CONFIG_FILE -Pattern "OUTPUT_DIR=" -Quiet) {
			(Get-Content $CONFIG_FILE) -replace ".*OUTPUT_DIR=.*", "OUTPUT_DIR=$($config['OUTPUT_DIR'])" | Set-Content $CONFIG_FILE
		}
		else {
			Add-Content -Path $CONFIG_FILE -Value "OUTPUT_DIR=$($config['OUTPUT_DIR'])"
		}
	}
}

# Prompt the user whether or not to override the directory
function prompt_output_override() {
	while ($config["OVERWRITE"] -eq "" -and $config["OVERWRITE"] -ne $false) {
		$ans = Read-Host "If the directory exists, would you like to override its contents? (Yes/No, default: No)"
		switch ($ans) {
			{ @("y", "yes") -contains $_ } {
				$config["OVERWRITE"] = $true
			}
			{ @("", "n", "no") -contains $_ } {
				$config["OVERWRITE"] = $false
			}
			default {
				Write-Host "Answer must be Yes or No"
				continue
			}
		}
		
		# Add the response to the config file
		if (Select-String -Path $CONFIG_FILE -Pattern "OVERWRITE=" -Quiet) {
			(Get-Content $CONFIG_FILE) -replace ".*OVERWRITE=.*", "OVERWRITE=$($config['OVERWRITE'])" | Set-Content $CONFIG_FILE
		}
		else {
			Add-Content -Path $CONFIG_FILE -Value "OVERWRITE=$($config['OVERWRITE'])"
		}
		
	}
}

# Prompt the user for the ping page url
function prompt_url() {
	while ($config["URL"] -eq "") {
		# Autodetect URL by checking the following URLS
		# https://localhost:{port}/FileNet/Engine
		# https://{$Env:computername}:{port}/FileNet/Engine
		
		# Find the ping page port
		if (Test-Path "$($config['WAS_ROOT_DIR'])/profiles") {
			Write-Host "Searching for URL port number..."
			# This search takes a long time
			$port_config = Join-Path -Path "$($config['WAS_ROOT_DIR'])/profiles" -ChildPath ((Get-ChildItem "$($config['WAS_ROOT_DIR'])/profiles" -Name 'portdef.props' -Recurse) | Select-Object -First 1)
		}
		$detected_url = ""
		
		# Try to autodetect the url
		if ($port_config -ne $null) {
			Write-Host "Trying to autodetect url..."
			$port = Select-String -Pattern "WC_defaulthost_secure" -Path $port_config | Select-Object -ExpandProperty Line | ForEach-Object { [regex]::matches($_, '\d+').value }
			
			$url = "https://localhost:${port}/FileNet/Engine"
			$status = [int][System.Net.WebRequest]::Create($url).GetResponse().StatusCode
			if ($status -eq 200) {
				$detected_url = $url
			}
			
			$url = [string]::Format('https://{0}:{1}/FileNet/Engine', $Env:computername, $port)
			$status = [int][System.Net.WebRequest]::Create($url).GetResponse().StatusCode
			if ($status -eq 200) {
				$detected_url = $url
			}
		}
		
		if ($detected_url -eq "") {
			$ans = Read-Host "Please input the URL for your ping page"
		}
		else {
			$ans = Read-Host "Please input the URL for your ping page (default: ${detected_url})"
			
			if ($ans -eq "") {
				$ans = $detected_url
			}
		}
		
		if ($ans -eq "") {
			Write-Host "Blank URL. Please try again."
			continue
		}
		
		# Check the status of the inputted url
		$status = [int][System.Net.WebRequest]::Create($ans).GetResponse().StatusCode
		if ($status -ne 200) {
			Write-Host "The URL was not reachable. Please try again."
			continue
		}
		
		$config["URL"] = $ans
		
		# Add the response to the config file
		if (Select-String -Path $CONFIG_FILE -Pattern "URL=" -Quiet) {
			(Get-Content $CONFIG_FILE) -replace ".*URL=.*", "URL=$($config['URL'])" | Set-Content $CONFIG_FILE
		}
		else {
			Add-Content -Path $CONFIG_FILE -Value "URL=$($config['URL'])"
		}
	}
}

# Prompt user whether or not to run the script in verbose mode
function prompt_verbose() {
	while ($config["VERBOSE"] -eq "" -and $config["VERBOSE"] -ne $false) {
		Write-Host $config["VERBOSE"]
		$ans = Read-Host "Run in verbose mode? (Yes/No, default: No)"
		switch ($ans) {
			{ @("y", "yes") -contains $_ } {
				$config["VERBOSE"] = $true
			}
			{ @("", "n", "no") -contains $_ } {
				$config["VERBOSE"] = $false
			}
			default {
				Write-Host "Answer must be Yes or No"
				continue
			}
		}
		
		# Add the response to the config file
		if (Select-String -Path $CONFIG_FILE -Pattern "VERBOSE=" -Quiet) {
			(Get-Content $CONFIG_FILE) -replace ".*VERBOSE=.*", "VERBOSE=$($config['VERBOSE'])" | Set-Content $CONFIG_FILE
		}
		else {
			Add-Content -Path $CONFIG_FILE -Value "VERBOSE=$($config['VERBOSE'])"
		}
		
	}
}

function log_error {
	Write-Host "[ERROR]: $($Args[0])"
}

function log_debug {
	if ($config["VERBOSE"] -ne $true) {
		return
	}

	Write-Host "[DEBUG]: $($Args[0])"
}

# Writes Args[0] to the file Args[1].
# If OVERWRITE is false, append a timestamp to Args[1]
function write_file() {
	if ($config["OVERWRITE"] -eq $false) {
		$timestamp = Get-Date -UFormat "%Y-%m-%d-%H%M%S"
		$directory = [System.IO.Path]::GetDirectoryName($Args[1])
		$filename = [System.IO.Path]::GetFileName($Args[1])
		$new_filepath = Join-Path -Path $directory -ChildPath "\${timestamp}-${filename}"
		$Args[0] | Out-File $new_filepath
		return
	}
	$Args[0] | Out-File $Args[1]
}

# Remove the output directory and compressed file if found.
function clean {
	log_debug "---- Cleaning Files ----"
	if (Test-Path $config["OUTPUT_DIR"]) {
		log_debug "Removing output directory."
		Remove-Item -Recurse -Force $config["OUTPUT_DIR"]
	}

	if (Test-Path "$($config['OUTPUT_DIR']).zip") {
		log_debug "Removing archive."
		Remove-Item -Force "$($config['OUTPUT_DIR']).zip"
	}
}

# Main function for copying logs and compressing output directory
function create {
	# Verify that all config options are set
	if ($null -eq $config["WAS_ROOT_DIR"] -or $config["WAS_ROOT_DIR"] -eq "") {
		log_error "Unable to locate your WebSphere root directory."
		return
	}
	if ($null -eq $config["URL"] -or $config["URL"] -eq "") {
		log_error "Unable to locate your ping page URL."
		return
	}
	if ($null -eq $config["OUTPUT_DIR"] -or $config["OUTPUT_DIR"] -eq "") {
		log_error "Unable to locate your output directory."
		return
	}
	if (($null -eq $config["VERBOSE"] -or $config["VERBOSE"] -eq "") -and $config["VERBOSE"] -ne $false) {
		log_error "Unable to determine whether or not to run in verbose mode."
		return
	}
	
	# First clean up any old folders
	if ($config["OVERWRITE"] -eq $true) {	
		clean
	}

	init_output_folder
	get_java_version
	get_ping_page
	get_ping_page_info
	get_logs
	create_archive
}

function init_output_folder {
	if (-not (Test-Path $config['OUTPUT_DIR'])) {
		New-Item -ItemType Directory -Force -Path $config['OUTPUT_DIR'] | Out-Null
		log_debug "Created output directory..."
	}
}

function get_java_version {
	log_debug "---- Getting Java Version ----"
	$java_version = (Get-Command java | Select-Object -ExpandProperty Version).toString()
	$file = Join-Path -Path $config['OUTPUT_DIR'] -ChildPath "\Java_Version.txt"
	write_file "${java_version}" $file
	log_debug "---- Successfully Found Java Version ----"
}

function get_ping_page {
	log_debug "---- Getting Ping Page ----"
	if (-not (Get-Command curl.exe -ErrorAction SilentlyContinue)) {
		log_error "curl.exe not found. Please install curl.exe or manually extract the ping page using instructions from the readme."
		return
	}
	$content = curl.exe -sk "$($config['URL'])"
	$file = Join-Path -Path $config['OUTPUT_DIR'] -ChildPath "\index.html"
	write_file "${content}" $file
	log_debug "---- Successfully Got Ping Page ----"
}

function get_ping_page_info {
	log_debug "---- Getting Ping Page Information ----"
	if (-not (Get-Command curl.exe -ErrorAction SilentlyContinue)) {
		log_error "curl.exe not found. Please install curl.exe or manually extract the ping page using instructions from the readme."
		return
	}

	$PING_PAGE_INFO = @{
		"JDBC Driver"        = "JDBC_DRIVER.txt"
		"Build Version"      = "Build_Version.txt"
		"P8 Domain"          = "P8_Domain.txt"
		"Server Instance{s}" = "Server_Instances.txt"
	}
	
	$page = (curl.exe -sk $config['URL'])
	
	$PING_PAGE_INFO.Keys | ForEach-Object {
		$str = $_
		$file_name = $PING_PAGE_INFO[$str]
		$file = Join-Path -Path $config['OUTPUT_DIR'] -ChildPath $file_name
		log_debug "Getting $str and outputting to $file"

		# Regex to get the corresponding value in the HTML table to a given key
		$value = ($page -match "${str}" | sed.exe "s/^.*${str}<\/TD><TD[^>]*>\([^<]*\)<\/TD>.*/\1/")
		
		if ($null -eq $value -or $value -eq "") {
			log_error "Unable to locate the ${str}"
			continue
		}
		
		log_debug "Found ${value}"
		write_file "${value}" "${file}"
	}
	log_debug "---- Successfully Got Ping Page Information ----"
}

function get_logs {
	log_debug "---- Getting Logs ----"
	
	if (-not (Test-Path -PathType Container -Path "$($config['WAS_ROOT_DIR'])\profiles")) {
		log_error "No profiles directory under $($config['WAS_ROOT_DIR'])"
		return
	}

	Get-ChildItem -Path (Join-Path -Path $config['WAS_ROOT_DIR'] -ChildPath "\profiles\*\") | ForEach-Object {
		$i = $_.FullName
		
		# ce_trace and ce_system logs
		if (Test-Path -PathType Container -Path (Join-Path -Path $i -ChildPath "\FileNet")) {
			Get-ChildItem -Path (Join-Path -Path $i -ChildPath "FileNet\*\") | ForEach-Object {
				$j = $_.FullName
				
				if (-not (Test-Path -Path $j -PathType Container)) {
					return
				}
				
				$output_log_folder = Join-Path -Path $config['OUTPUT_DIR'] -ChildPath (Split-Path -Path $i -Leaf) | Join-Path -ChildPath (Split-Path -Path $j -Leaf)
				
				if (-not (Test-Path $output_log_folder)) {
					log_debug "Creating ${output_log_folder}"
					New-Item -ItemType Directory -Force -Path $output_log_folder | Out-Null
				}

				Get-ChildItem -Path (Join-Path -Path $j -ChildPath "ce_system*.log") | ForEach-Object {
					$k = $_.FullName
					log_debug "Copying ${k} into ${output_log_folder}"
					
					$filename = [System.IO.Path]::GetFileName($k)
					$file = Join-Path -Path $output_log_folder -ChildPath $filename
					$content = Get-Content $k
					write_file "${content}" $file
				}

				Get-ChildItem -Path (Join-Path -Path $j -ChildPath "ce_trace*.log") | ForEach-Object {
					$k = $_.FullName
					log_debug "Copying ${k} into ${output_log_folder}"
					
					$filename = [System.IO.Path]::GetFileName($k)
					$file = Join-Path -Path $output_log_folder -ChildPath $filename
					$content = Get-Content $k
					write_file "${content}" $file
				}

				Get-ChildItem -Path (Join-Path -Path $j -ChildPath "pe_system*.log") | ForEach-Object {
					$k = $_.FullName
					log_debug "Copying ${k} into ${output_log_folder}"

					$filename = [System.IO.Path]::GetFileName($k)
					$file = Join-Path -Path $output_log_folder -ChildPath $filename
					$content = Get-Content $k
					write_file "${content}" $file
				}

				Get-ChildItem -Path (Join-Path -Path $j -ChildPath "pe_trace*.log") | ForEach-Object {
					$k = $_.FullName
					log_debug "Copying ${k} into ${output_log_folder}"
					
					$filename = [System.IO.Path]::GetFileName($k)
					$file = Join-Path -Path $output_log_folder -ChildPath $filename
					$content = Get-Content $k
					write_file "${content}" $file
				}
			}
		}

		# SystemOut logs
		if (Test-Path -PathType Container (Join-Path -Path $i -ChildPath "\logs")) {
			Get-ChildItem -Path (Join-Path -Path $i -ChildPath "\logs\*\") | ForEach-Object {
				$j = $_.FullName
				if (-not (Test-Path -Path $j -PathType Container)) {
					return
				}
				
				if (-not (Test-Path $j\SystemOut.log)) {
					log_debug "Unable to find ${j}\SystemOut.log"
					return
				}

				$output_log_folder = Join-Path -Path $config['OUTPUT_DIR'] -ChildPath (Split-Path -Path $i -Leaf) | Join-Path -ChildPath (Split-Path -Path $j -Leaf)

				if (-not (Test-Path $output_log_folder)) {
					log_debug "Creating ${output_log_folder}"
					New-Item -ItemType Directory -Force -Path $output_log_folder | Out-Null
				}

				log_debug "Copying ${j}\SystemOut.log into ${output_log_folder}"
				
				$filename = "SystemOut.log"
				$file = Join-Path -Path $output_log_folder -ChildPath $filename
				$content = Get-Content (Join-Path -Path $j -ChildPath "\SystemOut.log")
				write_file "${content}" $file
			}
		}

		# ffdc logs
		if (Test-Path -PathType Container (Join-Path -Path $i -ChildPath "logs\ffdc")) {
			Get-ChildItem -Path (Join-Path -Path $i -ChildPath "\logs\ffdc") | ForEach-Object {
				$j = $_.FullName
				$output_log_folder = Join-Path -Path $config['OUTPUT_DIR'] -ChildPath (Split-Path -Path $i -Leaf) | Join-Path -ChildPath "\ffdc"
				
				if (-not (Test-Path -PathType Container $output_log_folder)) {
					log_debug "Creating ${output_log_folder}"
					New-Item -ItemType Directory -Force -Path $output_log_folder | Out-Null
				}
				
				log_debug "Copying ${j} into ${output_log_folder}"
				$filename = [System.IO.Path]::GetFileName($j)
				$file = Join-Path -Path $output_log_folder -ChildPath $filename
				$content = Get-Content $j
				write_file "${content}" $file
				
			}
		}
	}

	log_debug "---- Successfully Copied Logs ----"
}

function create_archive {
	log_debug "---- Creating Archive ----"

	if (-not (Test-Path $config['OUTPUT_DIR'])) {
		log_error "Unable to locate $($config['OUTPUT_DIR'])"
		return
	}

	Compress-Archive -Force -Path "$($config['OUTPUT_DIR'])" -DestinationPath "$($config['OUTPUT_DIR']).zip"
	log_debug "---- Successfully Created Archive ----"
}

# Display Help message
function help {
	Write-Host "---- Help ----"
	Write-Host "Description: A Windows Powershell script used to collect WebSphere logs."
	Write-Host "Options:"
	Write-Host " .\windows-script.ps1           Creates the archive."
	Write-Host " .\windows-script.ps1 clean     Clean up all files."
	Write-Host " .\windows-script.ps1 help      Displays this message."
	Write-Host "Flags:"
	Write-Host " -i                             Run in interactive mode."
}

# Handle Interactive (-i) flag
if ($i) {
	$config["WAS_ROOT_DIR"] = ""
	$config["URL"] = ""
	$config["OUTPUT_DIR"] = ""
	$config["VERBOSE"] = ""
	$config["OVERWRITE"] = ""
}

switch ($action) {
	"clean" {
		prompt_output
		prompt_verbose
		clean
	}
	"help" { help }
	Default {
		prompt_was_root
		prompt_output
		prompt_output_override
		prompt_url
		prompt_verbose
		create
	}
}

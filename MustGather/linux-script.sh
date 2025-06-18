#!/bin/bash

# Config file to be read from.
CONFIG_FILE="./config"

declare -A config
config["WAS_ROOT_DIR"]=""
config["URL"]=""
config["OUTPUT_DIR"]=""
config["VERBOSE"]=""
config["OVERWRITE"]=""

# Read values from config file
if [[ ! -e $CONFIG_FILE ]]; then
    touch $CONFIG_FILE
fi
sed -i 's/\r//' $CONFIG_FILE
if [[ -r $CONFIG_FILE ]]; then
    while read line; do
        if echo $line | grep -F = &>/dev/null; then
            var=$(echo "$line" | cut -d '=' -f 1)
            config[$var]=$(echo "$line" | cut -d '=' -f 2- | xargs)
        fi
    done <$CONFIG_FILE
fi

# Curl status
curl_status=$(command -v curl)

# Prompt the user for the WebSphere directory
function prompt_was_root() {
    while [[ -z "${config['WAS_ROOT_DIR']}" ]]; do
        if [[ -z $WAS_HOME ]]; then
            printf "Please input the WebSphere directory:\n"
            read -rp "" ans
        else
            printf "Please input the WebSphere directory (default: ${WAS_HOME}):\n"
            read -rp "" ans

            if [[ -z $ans ]]; then
                ans=$WAS_HOME
            fi
        fi

        if [[ ! -e $ans ]]; then
            printf "This location does not exist. Please try again.\n"
            continue
        fi

        config["WAS_ROOT_DIR"]=$ans

        # Add the response to the config file
        exists=$(cat $CONFIG_FILE | grep "WAS_ROOT_DIR")
        if [[ -z $exists ]]; then
            echo "WAS_ROOT_DIR=${config['WAS_ROOT_DIR']}" >>$CONFIG_FILE
        else
            escaped=$(sed 's/[&/\]/\\&/g' <<<"$ans")
            sed -i "s/.*WAS_ROOT_DIR=.*/WAS_ROOT_DIR=${escaped}/" $CONFIG_FILE
        fi
    done
}

# Prompt the user for the output directory
function prompt_output() {
    while [[ -z "${config['OUTPUT_DIR']}" ]]; do
        printf "Please input the output directory:\n"
        read -rp "" ans

        config["OUTPUT_DIR"]=$ans

        # Add the response to the config file
        exists=$(cat $CONFIG_FILE | grep "OUTPUT_DIR")
        if [[ -z $exists ]]; then
            echo "OUTPUT_DIR=${config['OUTPUT_DIR']}" >>$CONFIG_FILE
        else
            escaped=$(sed 's/[&/\]/\\&/g' <<<"$ans")
            sed -i "s/.*OUTPUT_DIR=.*/OUTPUT_DIR=${escaped}/" $CONFIG_FILE
        fi
    done
}

# Prompt the user whether or not to override the directory
function prompt_output_override() {
    while [[ -z "${config['OVERWRITE']}" ]]; do
        printf "If the directory exists, would you like to override its contents? (Yes/No, default: No):\n"
        read -rp "" ans

        case "$ans" in
        "y" | "Y" | "yes" | "Yes" | "YES")
            config["OVERWRITE"]=true
            ;;
        "n" | "N" | "no" | "No" | "NO" | "")
            config["OVERWRITE"]=false

            ;;
        *)
            printf "Answer must be Yes or No\n"
            continue
            ;;
        esac

        # Add the response to the config file
        exists=$(cat $CONFIG_FILE | grep "OVERWRITE")
        if [[ -z $exists ]]; then
            echo "OVERWRITE=${config['OVERWRITE']}" >>$CONFIG_FILE
        else
            escaped=$(sed 's/[&/\]/\\&/g' <<<"${config['OVERWRITE']}")
            sed -i "s/.*OVERWRITE=.*/OVERWRITE=${escaped}/" $CONFIG_FILE
        fi
    done
}

# Prompt the user for the ping page url
function prompt_url() {
    while [[ -z "${config['URL']}" ]]; do
        # Autodetect URL by checking the following URLs
        # https://localhost:{port}/FileNet/Engine
        # https://{hostname}:{port}/FileNet/Engine

        # Find the ping page port
        if [[ -e "${config['WAS_ROOT_DIR']}/profiles" ]]; then
            port_config=$(cd "${config['WAS_ROOT_DIR']}/profiles" && find ~+ -name 'portdef.props' | head -1)
        fi
        detected_url=""

        # Try to autodetect the url
	if [[ -n $curl_status ]]; then
		if [[ -f "${port_config}" ]]; then
		    port=$(cat $port_config | grep "WC_defaulthost_secure" | sed 's/^.*=\([0-9]*\)/\1/')
		    url="https://localhost:${port}/FileNet/Engine"
		    status=$(curl -Isk $url 2>/dev/null | head -1 | awk '{print $2}')
		    if [[ $status == "200" ]]; then
			detected_url=$url
		    fi

		    url="https://${HOSTNAME}:${port}/FileNet/Engine"
		    status=$(curl -Isk $url 2>/dev/null | head -1 | awk '{print $2}')
		    if [[ $status == "200" ]]; then
			detected_url=$url
		    fi
		fi
	else
		log_error "curl not found. Please install curl or manually extract the ping page using instructions from the readme."
	fi

        if [[ -z $detected_url ]]; then
            printf "Please input the URL for your ping page:\n"
            read -rp "" ans
        else
            printf "Please input the URL for your ping page (default: ${detected_url}):\n"
            read -rp "" ans

            if [[ -z $ans ]]; then
                ans=$detected_url
            fi
        fi

        if [[ -z $ans ]]; then
            printf "Blank URL. Please try again.\n"
            continue
        fi

        # Check the status of the inputted url
	if [[ -n $curl_status ]]; then
		status=$(curl -Isk $ans 2>/dev/null | head -1 | awk '{print $2}')
		if [[ $status != "200" ]]; then
		    printf "The URL was not reachable. Please try again.\n"
		    continue
		fi
	fi

        config["URL"]=$ans

        # Add the response to the config file
        exists=$(cat $CONFIG_FILE | grep "URL")
        if [[ -z $exists ]]; then
            echo "URL=${config['URL']}" >>$CONFIG_FILE
        else
            escaped=$(sed 's/[&/\]/\\&/g' <<<"$ans")
            sed -i "s/.*URL=.*/URL=${escaped}/" $CONFIG_FILE
        fi
    done
}

# Prompt user whether or not to run the script in verbose mode.
function prompt_verbose() {
    while [[ -z "${config['VERBOSE']}" ]]; do
        printf "Run in verbose mode? (Yes/No, default: No):\n"
        read -rp "" ans
        case "$ans" in
        "y" | "Y" | "yes" | "Yes" | "YES")
            config["VERBOSE"]=true
            ;;
        "n" | "N" | "no" | "No" | "NO" | "")
            config["VERBOSE"]=false
            ;;
        *)
            printf "Answer must be Yes or No\n"
            continue
            ;;
        esac

        # Add the response to the config file
        exists=$(cat $CONFIG_FILE | grep "VERBOSE")
        if [[ -z $exists ]]; then
            echo "VERBOSE=${config['VERBOSE']}" >>$CONFIG_FILE
        else
            escaped=$(sed 's/[&/\]/\\&/g' <<<"${config['VERBOSE']}")
            sed -i "s/.*VERBOSE=.*/VERBOSE=${escaped}/" $CONFIG_FILE
        fi
    done
}

function log_error() {
    echo "[ERROR]: ${1}"
}

function log_debug() {
    if [[ ${config['VERBOSE']} == false ]]; then
        return
    fi

    echo "[DEBUG]: ${1}"
}

# Writes $1 to the file $2.
# If OVERWRITE is false, append a timestamp to $2
function write_file() {
    if [[ ${config['OVERWRITE']} == false ]]; then
        timestamp=$(date +'%Y-%m-%d-%H%M%S')
        directory=$(dirname $2)
        filename="$timestamp-$(basename $2)"
        echo "$1" >"$directory/$filename"
        return
    fi
    echo "$1" >"$2"
}

# Remove the output directory and compressed file if found.
function clean() {
    log_debug "---- Cleaning Files ----"
    if [[ -e ${config['OUTPUT_DIR']} ]]; then
        log_debug "Removing output directory."
        rm -rf "${config['OUTPUT_DIR']}"
    fi

    if [[ -e "${config['OUTPUT_DIR']}.tar.gz" ]]; then
        log_debug "Removing archive."
        rm -f "${config['OUTPUT_DIR']}.tar.gz"
    fi
}

# Main function for copying logs and compressing output directory
function create() {
    # Verify that all config options are set
    if [[ -z ${config['WAS_ROOT_DIR']} ]]; then
        log_error "Unable to locate your WebSphere root directory."
        return
    fi
    if [[ -z ${config['URL']} ]]; then
        log_error "Unable to locate your ping page URL."
        return
    fi
    if [[ -z ${config['OUTPUT_DIR']} ]]; then
        log_error "Unable to locate your output directory."
        return
    fi
    if [[ -z ${config['VERBOSE']} ]]; then
        log_error "Unable to determine whether or not to run in verbose mode."
        return
    fi

    if [[ ${config['OVERWRITE']} == true ]]; then
        # First clean up any old folders
        clean
    fi

    init_output_folder
    get_java_version
    get_ping_page
    get_ping_page_info
    get_logs
    create_archive
}

function init_output_folder() {
    if [[ ! -e ${config['OUTPUT_DIR']} ]]; then
        mkdir "${config['OUTPUT_DIR']}"
        log_debug "Created output directory..."
    fi
}

function get_java_version() {
    log_debug "---- Getting Java Version ----"
    java_version=$(java -version 2>&1)
    write_file "$java_version" "${config['OUTPUT_DIR']}/Java_Version.txt"
    log_debug "---- Successfully Found Java Version ----"
}

function get_ping_page {
    log_debug "---- Getting Ping Page ----"
    if [[ -z $curl_status ]]; then
	log_error "curl not found. Please install curl or manually extract the ping page using instructions from the readme."
	return
    fi
    content=$(curl -k "${config['URL']}" 2>/dev/null)
    write_file "$content" "${config['OUTPUT_DIR']}/index.html"
    log_debug "---- Successfully Got Ping Page ----"
}

function get_ping_page_info() {
    log_debug "---- Getting Ping Page Information ----"
    declare -A PING_PAGE_INFO
    if [[ -z $curl_status ]]; then
	log_error "curl not found. Please install curl or manually extract the ping page using instructions from the readme."
	return
    fi
    PING_PAGE_INFO["JDBC Driver"]="JDBC_Driver.txt"
    PING_PAGE_INFO["Build Version"]="Build_Version.txt"
    PING_PAGE_INFO["P8 Domain"]="P8_Domain.txt"
    PING_PAGE_INFO["Server Instance{s}"]="Server_Instances.txt"

    page=$(curl -k "${config['URL']}" 2>/dev/null)

    for str in "${!PING_PAGE_INFO[@]}"; do
        file="${config['OUTPUT_DIR']}/${PING_PAGE_INFO[$str]}"
        log_debug "Getting ${str} and outputting to ${file}"

        # Regex to get the corresponding value in the HTML table to a given key
        value=$(echo $page | grep "${str}" | sed "s/^.*${str}<\/TD><TD[^>]*>\([^<]*\)<\/TD>.*/\1/")

        if [[ -z $value ]]; then
            log_error "Unable to locate the ${str}."
            continue
        fi

        log_debug "Found ${value}"
        write_file "$value" "$file"
    done
    log_debug "---- Successfully Got Ping Page Information ----"
}

function get_logs() {
    log_debug "---- Getting Logs ----"

    if [[ ! -d ${config['WAS_ROOT_DIR']}/profiles ]]; then
        log_error "No profiles directory under ${config['WAS_ROOT_DIR']}"
        return
    fi

    if [[ ! -r ${config['WAS_ROOT_DIR']}/profiles ]]; then
	log_error "Cannot read directory ${config['WAS_ROOT_DIR']}/profiles. Are you sure you have read permissions?"
	return
    fi

    for i in ${config['WAS_ROOT_DIR']}/profiles/*/; do

        # ce_trace and ce_system logs
        if [[ -e $i/FileNet ]]; then
            for j in $i/FileNet/*/; do
                output_log_folder=${config['OUTPUT_DIR']}/$(basename $i)/$(basename $j)/
                if [[ ! -e $output_log_folder ]]; then
                    log_debug "Creating ${output_log_folder}"
                    mkdir -p $output_log_folder
                fi

                for k in $j/ce_system*.log; do
                    [ -e "$k" ] || continue
                    log_debug "Copying ${k} into ${output_log_folder}"
                    file="${output_log_folder}/$(basename $k)"
                    content=$(<$k)
                    write_file "$content" "$file"
                done

                for k in $j/ce_trace*.log; do
                    [ -e "$k" ] || continue
                    log_debug "Copying ${k} into ${output_log_folder}"
                    file="${output_log_folder}/$(basename $k)"
                    content=$(<$k)
                    write_file "$content" "$file"
                done

                for k in $j/pe_system*.log; do
                    [ -e "$k" ] || continue
                    log_debug "Copying ${k} into ${output_log_folder}"
                    file="${output_log_folder}/$(basename $k)"
                    content=$(<$k)
                    write_file "$content" "$file"
                done

                for k in $j/pe_trace*.log; do
                    [ -e "$k" ] || continue
                    log_debug "Copying ${k} into ${output_log_folder}"
                    file="${output_log_folder}/$(basename $k)"
                    content=$(<$k)
                    write_file "$content" "$file"
                done

            done
        fi

        # SystemOut logs
        if [[ -e $i/logs ]]; then
            for j in $i/logs/*/; do

                if [[ ! -e $j/SystemOut.log ]]; then
                    log_debug "Unable to find ${j}/SystemOut.log"
                    continue
                fi

                output_log_folder=${config['OUTPUT_DIR']}/$(basename $i)/$(basename $j)/

                if [[ ! -e $output_log_folder ]]; then
                    log_debug "Creating ${output_log_folder}"
                    mkdir -p $output_log_folder
                fi

                log_debug "Copying ${j}/SystemOut.log into ${output_log_folder}"
                file="${output_log_folder}/SystemOut.log"
                content=$(<$j/SystemOut.log)
                write_file "$content" "$file"
            done
        fi

        # ffdc logs
        if [[ -e $i/logs/ffdc ]]; then
            for j in $i/logs/ffdc/*; do
                output_log_folder="${config['OUTPUT_DIR']}/$(basename $i)/ffdc"
                if [[ ! -e $output_log_folder ]]; then
                    log_debug "Creating ${output_log_folder}"
                    mkdir -p $output_log_folder
                fi

                log_debug "Copying ${j} into ${output_log_folder}"
                file="${output_log_folder}/$(basename $j)"
                content=$(<$j)
                write_file "$content" "$file"
            done
        fi
    done

    log_debug "---- Successfully Copied Logs ----"
}

function create_archive() {
    log_debug "---- Creating Archive ----"

    if [[ ! -e ${config['OUTPUT_DIR']} ]]; then
        log_error "Unable to locate ${config['OUTPUT_DIR']}"
        return
    fi

    tar czf "${config['OUTPUT_DIR']}.tar.gz" "${config['OUTPUT_DIR']}"
    log_debug "---- Successfully Created Archive ----"
}

# Display Help message
function help() {
    echo "---- Help ----"
    echo "Description: A Linux Bash script used to collect WebSphere logs."
    echo "Options:"
    echo " ./linux-script.sh        Creates the archive."
    echo " ./linux-script.sh clean  Clean up all files."
    echo " ./linux-script.sh help   Displays this message."
    echo "Flags:"
    echo " -i                       Run in interactive mode."
}

# Handle Interactive (-i) flag
if [[ $1 == "-i" ]]; then
    config["WAS_ROOT_DIR"]=""
    config["URL"]=""
    config["OUTPUT_DIR"]=""
    config["VERBOSE"]=""
    config["OVERWRITE"]=""
    shift
fi

case $1 in
"clean")
    prompt_output
    prompt_verbose
    clean
    ;;
"help")
    help
    ;;
*)
    prompt_was_root
    prompt_output
    prompt_output_override
    prompt_url
    prompt_verbose
    create
    ;;
esac

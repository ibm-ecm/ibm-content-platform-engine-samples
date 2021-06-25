#/*
# IBM Confidential
# OCO Source Materials
# 5737-I23
# Copyright IBM Corp. 2021
# The source code for this program is not published or otherwise divested of its trade secrets, irrespective of what has been deposited with the U.S Copyright Office.
# */


# The Configuration Manager tool uses this script as input when configuring the
# WebSphere server.  In order to run a script, the tool generates a runtime
# script based on the contents of this input script.  The changes and additions 
# that the tool makes to this input script in order to run the runtime script
# are documented here in comments.  Similar changes must be made to a similar
# script file in order to run that script to manually configure WebSphere.
#
# Various variable assignments, with appropriate values, must be present in order
# for the rest of the script to run.  The following variable assignments, with
# some example values, are applicable.

#Websphere version
# For WebSphere 7.0, value is: 7.0
# For WebSphere 8.0, value is: 8.0
# For WebSphere 8.5, value is: 8.5
# For WebSphere 9.0, value is: 9.0
#set _wasVersion "7.0"

#WAS administrative console user
#set _admConsoleUser ""

#set this configuration as current user registry
#set _setCurrent "false"

#LDAP type
# for Active directory and WAS 7.0, value is: AD2003
# for Active directory and WAS 6.1, value is: AD
# for ADAM, value is: ADAM
# for CA Directory, value is: CUSTOM
# for eDirectory, value is: NDS
# for OID, value is: CUSTOM
# for Sun java, value is: SUNONE
# for Tivoli, value is: IDS6
#set _ldapType	"IDS6"

#LDAP server hostname
#set _ldapServerHost	""

#LDAP server port number
#set _ldapServerPort	""

#LDAP server SSL enabled
#set _sslEnabled	"false"

#Bind distinguished name
#set _ldapBindDN ""

#Bind password
#set _bindPassword ""

#Base entry distinguished name in realm
#set _baseEntryNDRealm ""

#Base entry distinguished name in repository
#set _baseEntryNDRepository 

#repository identifier
#set _repoId ""

#Login properties
#set _loginProperties "cn"

#Federated repository realm
#set _fedReposRealm "defaultWIMFileBasedRealm"

#Name of group membership attribute
#set _groupMembershipName ""

#Scope of group membership attribute
#set _groupMembershipScope "direct"

#to turn off SSL certificates used for server communication: values are: true or false
#set _turnoffSSLcerts ""

############################################

############################################
#proc to add/modify new Admin Console user
############################################
proc addAdminConsoleUser { userName } {
	puts "addAdminConsoleUser"
	global AdminConfig
	set adminRole [lindex [$AdminConfig getid /AuthorizationTableExt:admin-authz.xml/RoleAssignmentExt:/] 0]
	set users [lindex [$AdminConfig showAttribute $adminRole users] 0]
	foreach user $users {
		if { [lindex [split $user (] 0] == $userName } {
			set attrs [list [list name $userName]]
			$AdminConfig modify $user $attrs
			$AdminConfig save
			puts "Done setting Admin console user"
			return
		}
	}
	
	set attrs [list [list name $userName]]
	$AdminConfig create UserExt $adminRole $attrs
	$AdminConfig save
	puts "Done setting Admin console user"
}

############################################
# turnoff RMI/IIOP SSL
############################################
proc turnOffCSI {} {
	global AdminConfig
	puts "Turn off RMI/IIOP SSL"
	set tlayer [$AdminConfig list TransportLayer]
    set inbound_sqop [$AdminConfig showAttribute [lindex $tlayer 0] supportedQOP]
    set inbound_rqop [$AdminConfig showAttribute [lindex $tlayer 0] requiredQOP]
	$AdminConfig modify $inbound_sqop [list [list establishTrustInClient false]]
    $AdminConfig modify $inbound_rqop [list [list establishTrustInClient false]]
	$AdminConfig modify $inbound_sqop [list [list enableProtection false]]
    $AdminConfig modify $inbound_rqop [list [list enableProtection false]]
	set outbound_sqop [$AdminConfig showAttribute [lindex $tlayer 1] supportedQOP]
    set outbound_rqop [$AdminConfig showAttribute [lindex $tlayer 1] requiredQOP]
	$AdminConfig modify $outbound_sqop [list [list enableProtection false]]
    $AdminConfig modify $outbound_rqop [list [list enableProtection false]]
	$AdminConfig save
	
}

############################################
# set the federated reposity as the current user registry
############################################
proc SetFedRepositoriesAsCurrent {setCurrent} {
	puts "SetFedRepositoriesAsCurrent"
	if {$setCurrent != "true"} {
		puts "Do not change current active user registry"
		return
	}
	
	global AdminConfig
	set userR [$AdminConfig list UserRegistry]
	set security [$AdminConfig list Security]
	foreach ur $userR {
		if { [regexp "WIM" $ur] } {
			set wim $ur
			break
		}
	}	
	set activeUR [list activeUserRegistry $wim]
	set secAttrs [list $activeUR]
	$AdminConfig modify $security $secAttrs
	$AdminConfig save
}

global AdminTask 
if {$_domainNotSet == "true"} {

puts "Add BaseEntry" 
catch {
	$AdminTask createIdMgrLDAPRepository [subst {-id $_repoId -ldapServerType $_ldapType }] 
} throwAway
puts $throwAway
$AdminTask addIdMgrLDAPServer [subst {-id $_repoId -host $_ldapServerHost -port $_ldapServerPort -bindDN " $_ldapBindDN " -bindPassword "$_bindPassword" -ldapServerType $_ldapType -sslEnabled $_sslEnabled}]
$AdminTask addIdMgrRepositoryBaseEntry [subst {-id $_repoId  -name " $_baseEntryNDRealm " -nameInRepository " $_baseEntryNDRepository "}]
$AdminTask updateIdMgrLDAPRepository [subst {-id $_repoId -loginProperties $_loginProperties }]
puts "Add LDAP base entry to federated repositories."
$AdminTask addIdMgrRealmBaseEntry [subst {-name $_fedReposRealm  -baseEntry " $_baseEntryNDRealm "}]
puts "Set group attribute definition."
$AdminTask setIdMgrLDAPGroupConfig [subst {-id $_repoId -name $_groupMembershipName -scope $_groupMembershipScope}]
$AdminConfig save 
puts "Done configuring Authenticator"
}

SetFedRepositoriesAsCurrent $_setCurrent

if {$_turnoffSSLcerts == "true"} {
	turnOffCSI
}

catch { addAdminConsoleUser $_admConsoleUser } throwAwayMsg



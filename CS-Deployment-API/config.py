#  Licensed Materials - Property of IBM (c) Copyright IBM Corp. 2024 All Rights Reserved.

#  US Government Users Restricted Rights - Use, duplication or disclosure restricted by GSA ADP Schedule Contract with
#  IBM Corp.

#  DISCLAIMER OF WARRANTIES :

#  Permission is granted to copy and modify this Sample code, and to distribute modified versions provided that both the
#  copyright notice, and this permission notice and warranty disclaimer appear in all copies and modified versions.

#  THIS SAMPLE CODE IS LICENSED TO YOU AS-IS. IBM AND ITS SUPPLIERS AND LICENSORS DISCLAIM ALL WARRANTIES, EITHER
#  EXPRESS OR IMPLIED, IN SUCH SAMPLE CODE, INCLUDING THE WARRANTY OF NON-INFRINGEMENT AND THE IMPLIED WARRANTIES OF
#  MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE. IN NO EVENT WILL IBM OR ITS LICENSORS OR SUPPLIERS BE LIABLE FOR
#  ANY DAMAGES ARISING OUT OF THE USE OF OR INABILITY TO USE THE SAMPLE CODE, DISTRIBUTION OF THE SAMPLE CODE, OR
#  COMBINATION OF THE SAMPLE CODE WITH ANY OTHER CODE. IN NO EVENT SHALL IBM OR ITS LICENSORS AND SUPPLIERS BE LIABLE
#  FOR ANY LOST REVENUE, LOST PROFITS OR DATA, OR FOR DIRECT, INDIRECT, SPECIAL, CONSEQUENTIAL, INCIDENTAL OR PUNITIVE
#  DAMAGES, HOWEVER CAUSED AND REGARDLESS OF THE THEORY OF LIABILITY, EVEN IF IBM OR ITS LICENSORS OR SUPPLIERS HAVE
#  BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.

##Replace all variables noted to match with system configuration##

# Change variables in this block to match with GQL system
# ---------------------------------------------------------------------------------#
GQL_URL = "REPLACE"
OS_NAME = "REPLACE"  # ObjectStore Name
# ---------------------------------------------------------------------------------#

# Change variables in this block to match with Source GraphQL Connection
# ---------------------------------------------------------------------------------#
# OAuth Auth | Use for IDP/SCIM
TOKEN_URL = "https://{oauth-provider-url}/idprovider/v1/auth/identitytoken"  # Replace value with URL to fetch token. If CP4BA, this is IAM URL
GRANT_TYPE = "REPLACE"  # Grant type for OAUTH, common value is: ["password"]
SCOPE = "REPLACE"  # Scope for OAUTH, common value is: ["openid"]
CLIENT_ID = "REPLACE"
CLIENT_SECRET = "REPLACE"
OAUTH_USERNAME = "REPLACE"
OAUTH_PASSWORD = "REPLACE"
# This values are necessary only IF using IDP/SCIM
EXCHANGE_TOKEN_URL = (
    "https://{cp4ba-host}/v1/preauth/validateAuth"  # Token exchange URL
)
# ---------------------------------------------------------------------------------#
# Basic Auth | Use for LDAP Direct Authentication
BASIC_USERNAME = "REPLACE"
BASIC_PASSWORD = "REPLACE"

# Change variables in this block to match with Target GraphQL Connection
# ---------------------------------------------------------------------------------#
# OAuth Auth
TARGET_TOKEN_URL = "https://{oauth-provider-url}/idprovider/v1/auth/identitytoken"  # Replace value with URL to fetch token. If CP4BA, this is IAM URL
TARGET_GRANT_TYPE = "REPLACE"  # Grant type for OAUTH, common values are: ["password"]
TARGET_SCOPE = "REPLACE"  # Scope for OAUTH, common value is: ["openid"]
TARGET_CLIENT_ID = "REPLACE"
TARGET_CLIENT_SECRET = "REPLACE"
TARGET_OAUTH_USERNAME = "REPLACE"
TARGET_OAUTH_PASSWORD = "REPLACE"
# This values are necessary only IF using IDP/SCIM
TARGET_EXCHANGE_TOKEN_URL = (
    "https://{cp4ba-host}/v1/preauth/validateAuth"  # Token exchange URL
)
# ---------------------------------------------------------------------------------#
# Basic Auth
TARGET_BASIC_USERNAME = "REPLACE"
TARGET_BASIC_PASSWORD = "REPLACE"

# Change variables in this block to match with Target GQL system
# ---------------------------------------------------------------------------------#
TARGET_GQL_URL = "REPLACE"
TARGET_OS_NAME = "REPLACE"
# ---------------------------------------------------------------------------------#


# Change variables in this block to match with Source APIC
# ---------------------------------------------------------------------------------#
# APIC Auth
APIC_TOKEN_URL = "REPLACE"
SERVICE_USER_ID = "REPLACE"  # Generated Service ID
SERVICE_USER_API_KEY = "REPLACE"  # Generated API Key for Service ID
# ---------------------------------------------------------------------------------#
# Change variables in this block to match with Target APIC
# ---------------------------------------------------------------------------------#
# APIC Auth
TARGET_APIC_TOKEN_URL = "REPLACE"
TARGET_SERVICE_USER_ID = "REPLACE"  # Generated Service ID
TARGET_SERVICE_USER_API_KEY = "REPLACE"  # Generated API Key for Service ID
# ---------------------------------------------------------------------------------#

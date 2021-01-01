Using fedcloudclient as command-lien client
===========================================

fedcloudclient has four groups of commands: "fedcloud token" for interactions with EGI CheckIn and access tokens,
"fedcloud endpoint" for interactions with GOCDB (and site endpoints according to GOCDB), "fedcloud site" for
manipulation with site configurations, and "fedcloud openstack" or "fedcloud openstack-int" for performing
Openstack commands on sites.

Authentication
**************

Many fedcloud commands need access token for authentication. Users can choose whether to provide access token
directly (via option "--checkin-access-token"), or using refresh token (must be provided together with
CheckIn client ID and secret) to generate access token on the fly.

The default OIDC identity provider is EGI CheckIn (https://aai.egi.eu/oidc). Users can set other OIDC identity
provider via option "--checkin-url".

Environment variables
********************

Most of fedcloud options, including token can be set via environment variables:

+-----------------------------+---------------------------------+
|     Environment variable    |   Command-line options          |
+=============================+=================================+
|    CHECKIN_ACCESS_TOKEN     |   --checkin-access-token        |
+-----------------------------+---------------------------------+
|    CHECKIN_REFRESH_TOKEN    |   --checkin-refresh-token       |
+-----------------------------+---------------------------------+
|    CHECKIN_CLIENT_ID        |   --checkin-client-id           |
+-----------------------------+---------------------------------+
|    CHECKIN_CLIENT_SECRET    |   --checkin-client-secret       |
+-----------------------------+---------------------------------+
|    CHECKIN_URL              |   --checkin-url                 |
+-----------------------------+---------------------------------+
|    EGI_SITE                 |   --site                        |
+-----------------------------+---------------------------------+
|    EGI_VO                   |   --vo                          |
+-----------------------------+---------------------------------+

For convenience, always set the frequently used options like token via environment, that can save a lot of time.

fedcloud --help command
***********************

"fedcloud --help" command will print help message. When using it in combination with other
commands, e.g. "fedcloud token --help", "fedcloud token check --hep", it will print list of options for the
corresponding commands

fedcloud token commands
***********************

"fedcloud token check --checkin-access-token <ACCESS_TOKEN>" : Check the expiration time of access token, so users can know whether
they need to refresh it.

"fedcloud token list-vos --checkin-access-token <ACCESS_TOKEN>" : Print the list of VO memberships according to the EGI CheckIn

fedcloud endpoint commands
**************************





fedcloud site commands
**********************
"fedcloud site" commands will read site configurations and manipulate with them. If the local site configurations exist
at ~/.fedcloud-site-config/, it will read them from there, otherwise the commands will read from `GitHub repository
<https://github.com/EGI-Foundation/fedcloud-catchall-operations/tree/master/sites>`_

"fedcloud site save-config" : Read the default site configurations from GitHub
and save them to ~/.fedcloud-site-config/ directory. That will speed-up reading site configurations and also enables
users to make customized site setting. The command will overwrite existing site configurations in the local directory.

"fedcloud site list" : List of existing sites in the site configurations

"fedcloud site show --site <SITE>" : Show configuration of the corresponding site.

"fedcloud site show-all" : Show configurations of all sites.

"fedcloud site show-project-id --site <SITE> --vo <VO>": show the project ID of the VO on the site.

fedcloud openstack commands
***************************

"fedcloud openstack --site <SITE> --vo <VO> --checkin-access-token <ACCESS_TOKEN> <OPENSTACK_COMMAND>" : perform an
Openstack command on the site and VO. Examples of Openstack commands are "image list", "server list" and can be used
with additional options for the commands, e.g. "image list --long", "server list --format json". The list of all
Openstack commands, and their parameters/usages are available
`here <https://docs.openstack.org/python-openstackclient/latest/cli/command-list.html>`_.

"fedcloud openstack-int --site <SITE> --vo <VO> --checkin-access-token <ACCESS_TOKEN>" : Call Openstack client without
command, so users can work interactively. OIDC authentication is done only once at the beginning, then the keystone
token is cached and will be used for successive commands without authentication via CheckIn again.




Using fedcloudclient as command-lien client
===========================================

**fedcloudclient** has four groups of commands: **"fedcloud token"** for interactions with EGI CheckIn and access tokens,
**"fedcloud endpoint"** for interactions with GOCDB (and site endpoints according to GOCDB), **"fedcloud site"** for
manipulation with site configurations, and **"fedcloud openstack"** or **"fedcloud openstack-int"** for performing
Openstack commands on sites.

Authentication
**************

Many **fedcloud** commands need access token for authentication. Users can choose whether to provide access token
directly (via option *"--checkin-access-token"*), or using refresh token (must be provided together with
CheckIn client ID and secret) to generate access token on the fly.

The default OIDC identity provider is EGI CheckIn (https://aai.egi.eu/oidc). Users can set other OIDC identity
provider via option *"--checkin-url"*.

Environment variables
*********************

Most of fedcloud options, including options for tokens can be set via environment variables:

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

For convenience, always set the frequently used options like tokens via environment variable, that can save a lot of time.

fedcloud --help command
***********************

**"fedcloud --help"** command will print help message. When using it in combination with other
commands, e.g. **"fedcloud token --help"**, **"fedcloud token check --hep"**, it will print list of options for the
corresponding commands

::

    $ fedcloud --help
    Usage: fedcloud [OPTIONS] COMMAND [ARGS]...

    Options:
      --help  Show this message and exit.

    Commands:
      endpoint       Endpoint command group for interaction with GOCDB and endpoints
      openstack      Executing Openstack commands on site and VO
      openstack-int  Interactive Openstack client on site and VO
      site           Site command group for manipulation with site configurations
      token          Token command group for manipulation with tokens


fedcloud token commands
***********************

**"fedcloud token check --checkin-access-token <ACCESS_TOKEN>"**: Check the expiration time of access token, so users can know whether
they need to refresh it. As mentioned before, access token may be given via environment variable *CHECKIN_ACCESS_TOKEN*

::

    $ fedcloud token check
    Access token is valid to 2021-01-02 01:25:39 UTC
    Access token expires in 3571 seconds


**"fedcloud token list-vos --checkin-access-token <ACCESS_TOKEN>"** : Print the list of VO memberships according to the EGI CheckIn

::

    $ fedcloud token list-vos
    eosc-synergy.eu
    fedcloud.egi.eu
    training.egi.eu



fedcloud endpoint commands
**************************





fedcloud site commands
**********************
**"fedcloud site"** commands will read site configurations and manipulate with them. If the local site configurations exist
at *~/.fedcloud-site-config/*, **fedcloud** will read them from there, otherwise the commands will read from `GitHub repository
<https://github.com/EGI-Foundation/fedcloud-catchall-operations/tree/master/sites>`_.

By default, **fedcloud** does not save anything on local disk, users have to save the site configuration to local disk
explicitly via **"fedcloud site save-config"** command. The advantage of having local
site configurations, beside faster loading, is to give users ability to make customizations, e.g. add additional VOs,
remove sites they do not have access, and so on.

**"fedcloud site save-config"** : Read the default site configurations from GitHub
and save them to *~/.fedcloud-site-config/* local directory. The command will overwrite existing site configurations
in the local directory.

::

    $$ fedcloud site save-config
    Saving site configs to directory /home/viet/.fedcloud-site-config


**"fedcloud site list"** : List of existing sites in the site configurations

::

    $ fedcloud site list
    100IT
    BIFI
    CESGA
    ...

**"fedcloud site show --site <SITE>"** : Show configuration of the corresponding site.

::

    $ fedcloud site show --site IISAS-FedCloud
    {
      "endpoint": "https://cloud.ui.savba.sk:5000/v3/",
      "gocdb": "IISAS-FedCloud",
      "vos": [
        {
          "auth": {
            "project_id": "a22bbffb007745b2934bf308b0a4d186"
          },
          "name": "covid19.eosc-synergy.eu"
        },
        ...


**"fedcloud site show-all"** : Show configurations of all sites.

**"fedcloud site show-project-id --site <SITE> --vo <VO>"**: show the project ID of the VO on the site.

::

    $ fedcloud site show-project-id --site IISAS-FedCloud --vo eosc-synergy.eu
     Endpoint : https://cloud.ui.savba.sk:5000/v3/
     Project ID : 51f736d36ce34b9ebdf196cfcabd24ee


fedcloud openstack commands
***************************

**"fedcloud openstack --site <SITE> --vo <VO> --checkin-access-token <ACCESS_TOKEN> <OPENSTACK_COMMAND>"** : perform an
Openstack command on the site and VO. Examples of Openstack commands are *"image list"*, *"server list"* and can be used
with additional options for the commands, e.g. *"image list --long"*, *"server list --format json"*. The list of all
Openstack commands, and their parameters/usages are available
`here <https://docs.openstack.org/python-openstackclient/latest/cli/command-list.html>`_.

::

    $ fedcloud openstack image list --site IISAS-FedCloud --vo eosc-synergy.eu
    Site: IISAS-FedCloud, VO: eosc-synergy.eu
    +--------------------------------------+-------------------------------------------------+--------+
    | ID                                   | Name                                            | Status |
    +--------------------------------------+-------------------------------------------------+--------+
    | 862d4ede-6a11-4227-8388-c94141a5dace | Image for EGI CentOS 7 [CentOS/7/VirtualBox]    | active |

**"fedcloud openstack-int --site <SITE> --vo <VO> --checkin-access-token <ACCESS_TOKEN>"** : Call Openstack client without
command, so users can work interactively. OIDC authentication is done only once at the beginning, then the keystone
token is cached and will be used for successive commands without authentication via CheckIn again.

::

    $ fedcloud openstack-int --site IISAS-FedCloud --vo eosc-synergy.eu
    (openstack) image list
    +--------------------------------------+-------------------------------------------------+--------+
    | ID                                   | Name                                            | Status |
    +--------------------------------------+-------------------------------------------------+--------+
    | 862d4ede-6a11-4227-8388-c94141a5dace | Image for EGI CentOS 7 [CentOS/7/VirtualBox]    | active |
    ...
    (openstack) flavor list
    +--------------------------------------+-----------+-------+------+-----------+-------+-----------+
    | ID                                   | Name      |   RAM | Disk | Ephemeral | VCPUs | Is Public |
    +--------------------------------------+-----------+-------+------+-----------+-------+-----------+
    | 5bd8397c-b97f-462d-9d2b-5b533844996c | m1.small  |  2048 |   10 |         0 |     1 | True      |
    | df25f80f-ed19-4e0b-805e-d34620ba0334 | m1.medium |  4096 |   40 |         0 |     2 | True      |
    ...
    (openstack)






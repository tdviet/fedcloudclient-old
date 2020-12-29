FedCloud client: Command-line client and library for EGI Federated Cloud
========================================================================

*fedcloud* command-line client is based on
[egicli](https://github.com/EGI-Foundation/egicli), a simple
command-line interface and library for interacting with some of the
services of EGI. The *fedcloud* command-line client extends the
functionalities for interaction directly with Openstack sites in EGI
Federated Cloud and perform commands on sites in the same way as the
local in-site *openstack* client.

*fedcloud* client uses the same Openstack commands and options as
*openstack* client. It uses site IDs and VOs for setting site/project
that greatly improve user experiences and virtually makes EGI Federated
Cloud look like single unified Cloud.

Example of using *openstack* client for listing VMs in a project in a
site:

    openstack server list -os-auth-url SITE_ENDPOINT --os-project-id PROJECT_ID -os-access-toke ACCESS_TOKEN
    --os-auth-type v3oidcaccesstoken --os-protocol openid --os-identity-provider egi.eu

With *fedcloud* client:

    fedcloud openstack server list --site SITE_ID --vo VO --checkin-access-token ACCESS_TOKEN

The full set of *openstack* client commands is described
[here](https://docs.openstack.org/python-openstackclient/latest/cli/command-list.html).

Beside using as command-line client, fedcloud client can be used as
development library for developers of tools and services for EGI
Federated Cloud. See the demo code [*"demo.py"*](https://github.com/tdviet/fedcloudclient/blob/fedcloud-client/examples/demo.py)
to see how the library is used.

Quick start
-----------

-   Install FedCloud client is via *pip*:

<!-- -->

    $ pip3 install fedcloudclient

or use Docker container:

<!-- -->

    $ docker run -it  tdviet/fedcloudclient bash

-   Get a new access token from EGI Check-in according to instructions from
    FedCloud [Check-in client](https://aai.egi.eu/fedcloud/).
    

-   Check the expiration time of the access token using *fedcloud*
    command:

<!-- -->

    $ fedcloud token check --checkin-access-token <ACCESS_TOKEN>

-   List the VO memberships of the access token:

<!-- -->

    $ fedcloud token list-vos --checkin-access-token <ACCESS_TOKEN>

-   List the Openstack sites available in EGI Federated Cloud. That may
    take few seconds because all site configurations are retrieved from
    [GitHub repository](https://github.com/EGI-Foundation/fedcloud-catchall-operations/tree/master/sites)

<!-- -->

    $ fedcloud site list

-   Save the site configuration to local machine at
    *\~/.fedcloud-site-config/* to speed up the client's start in the
    next time:

<!-- -->

    $ fedcloud site save-config

-   Perform an Openstack command, e.g. list images in fedcloud.egi.eu VO on CYFRONET-CLOUD site (or other
    combination of site and VO you have access):

<!-- -->

    $ fedcloud openstack image list --site CYFRONET-CLOUD --vo fedcloud.egi.eu --checkin-access-token <ACCESS_TOKEN>

-   Set environment variable for access token, so you don't have to specify access token again and again. 
    The commands are much simpler now:

<!-- -->

    $ export CHECKIN_ACCESS_TOKEN=<ACCESS_TOKEN>

    $ fedcloud token check

    $ fedcloud openstack image list --site CYFRONET-CLOUD --vo fedcloud.egi.eu

-   Learn more commands of *fedcloud* client and experiment with them:

<!-- -->

    $ fedcloud --help

    $ fedcloud site --help

-   Experiment with more Openstack commands, e.g. *"fedcloud openstack
    server list"*. The full list of Openstack commands are available
    [here](https://docs.openstack.org/python-openstackclient/latest/cli/command-list.html)
    or via command *"openstack help"*.

Using fedcloudclient as development library
-------------------------------------------

All functionalities offered by the *fedcloud* client can be used as a
library for development of other tools and services for EGI Federated
Cloud. For example, performing openstack command as a function in
Python:

    from fedcloudclient.openstack import fedcloud_openstack
    ....
    json_object = fedcloud_openstack(
        checkin_access_token,
        site,
        vo,
        openstack_command)

See a working example [*"demo.py"*](https://github.com/tdviet/fedcloudclient/blob/fedcloud-client/examples/demo.py). 
The documentation of fedcloudclient API is available at [readthedocs.io](https://fedcloudclient.readthedocs.io/en/fedcloud-client/).

FAQ
---

1.  The *fedcloud* client is slow.

> Execute command *"fedcloud site save-config"* to download site
> configurations from
> [GitHub repository](https://github.com/EGI-Foundation/fedcloud-catchall-operations/tree/master/sites)
> and save them on a local machine. That will significantly speedup site
> configurations loading.
> 
> Some sites in the repository may not respond, and client has to wait for long time before report 
> "Connection time out". You can remove the sites from your local repository to speed-up all-sites operations

2.  The *fedcloud* client fails with error message *"SSL exception
    connecting to <https://> ..."* when attempts to interact with some
    sites.

> Some sites use certificates issued by national grid CAs that are not
> included in default distribution, so *fedcloud* client cannot verify
> them. Follow this [instruction](https://github.com/tdviet/python-requests-bundle-certs/blob/main/docs/Install_certificates.md)
> to install [EGI Core Trust Anchor](http://repository.egi.eu/category/production/cas/) and add
> certificates to Python request certificate bundle.
> 
> In the case of using virtual environment for quick test, you can download 
> and import bundle certificates by using
> the script from [this repository](https://github.com/tdviet/python-requests-bundle-certs)

3.  The *fedcloud* client fails with error message *"VO XX not found on site YY"* but they do exist.

> Site configurations at
> [GitHub repository](https://github.com/EGI-Foundation/fedcloud-catchall-operations/tree/master/sites)
> may be incomplete. Check the site configurations stored in
> *\~/.fedcloud-site-config/* if the VOs are included. If not, you can
> ask site admins to fix site configuration. You can also execute
> *"fedcloud endpoint projects --site SITE --checkin-access-token
> ACCESS\_TOKEN"* to find project IDs of the VOs on the site and add the VOs to
> local site configuration on your machine manually.

4.  I would like to add supports for additional sites/VOs/identity
    providers that are not parts of EGI Federated Cloud.

> Other identity providers may be specified via option *"--checkin-url"*
> or environment variable *"CHECKIN\_OIDC\_URL"*. Additional sites and
> VOs may be added to local site configuration files.

5.  Why there are options for both access token and refresh token? Which
    one should be used?

> Cloud operations need only access tokens, not refresh tokens. If a
> refresh token is given as parameter to *fedcloud* client (together
> with client ID and client secret), an access token will be generated
> on the fly from the refresh token and client ID/secret.
>
> Refresh tokens have long lifetime (one year in EGI CheckIn), so they
> should be securely protected. In secured environment, e.g. private
> computers, refresh tokens may be conveniently specified via environment
> variables *CHECKIN\_REFRESH\_TOKEN*, *CHECKIN\_CLIENT\_ID*,
> *CHECKIN\_CLIENT\_SECRET*; so users don't have to set token for
> *fecloud* client via command-line parameters.
>
> Access tokens have short lifetime (one hour in EGI CheckIn), so they
> have lower security constraints. However, they have to be refreshed
> frequently, that may be inconvenient for some users. In shared
> environment, e.g. VMs in Cloud, access tokens should be used instead
> of refreshed tokens.

=========================================================================
FedCloud client:  Command-line client and library for EGI Federated Cloud
=========================================================================

*fedcloud* client is based on `egicli <https://github.com/EGI-Foundation/egicli>`_, a simple command line interface
and library for interacting with some of the services of EGI. The *fedcloud* command-line client extends the
functionalities for interaction directly with Openstack sites in EGI Federated Cloud and perform commands on sites
like the standard *openstack* client.

Quick start
===========

- Install FedCloud client is via *pip*:

::

   $ pip install fedcloudclient

- Get a refreshed access token from Check-in according to instruction from
  FedCloud `Check-in client <https://aai.egi.eu/fedcloud/>`_.

- Check the validity of the access token using *fedcloud* command:

::

   $ fedcloud token check --checkin-access-token ACCESS_TOKEN

- List the VO memberships of the access token:

::

   $ fedcloud token list-vos --checkin-access-token ACCESS_TOKEN

- List the Openstack sites available in EGI Federated Cloud. That may take few seconds because all site configurations
  are retrieved from GitHub.

::

    $ fedcloud site list


- Save the site configuration to local machine at *~/.fedcloud-site-config/* to speed up the client's start in the next
  time:

::

    $ fedcloud site save-config

- Listing VMs in fedcloud.egi.eu VO on CESNET-MCC site:

::

    $ fedcloud openstack server list --site CESNET-MCC --vo fedcloud.egi.eu --checkin-access-token ACCESS_TOKEN

- Get some helps from the command-line client and experiment with them:

::

    $ fedcloud --help
    $ fedcloud openstack --help
    $ fedcloud site --help

FAQ
===

1. The *fedcloud* client is very slow.

 Execute command *"fedcloud site save-config"* to download site configurations from GitHub and save them on local machine.
 That will significantly speedup site configurations loading.

2. The *fedcloud* client fails with error message *"SSL exception connecting to https:// ..."* when attempts to
   interact with some sites.

  Some sites use certificates issued by national grid CAs that are not included in default distribution, so *fedcloud*
  client cannot verify them. Follow instructions in documentation to install `EGI Core Trust Anchor
  <http://repository.egi.eu/category/production/cas/>`_ and add certificates to Python request certificate bundle.

3. The *fedcloud* client fails with error message *"Site XX or VO YY not found"* but they do exist.

  Site configurations may be incomplete. Check the site configurations stored in *~/.fedcloud-site-config/* if the VOs
  are included. Execute *"fedcloud endpoint projects --site SITE --checkin-access-token ACCESS_TOKEN"* to find project
  IDs and add the VOs to site configuration manually.

4. I would like to add supports for additional sites/VOs/identity providers that are not parts of EGI Federated Cloud.

  Other identity providers may be specified via option *"--checkin-url"* or environment variable *"CHECKIN_OIDC_URL"*.
  Additional sites and VOs may be added to local site configuration files.

5. Why there are options for both access token and refresh token? Which one should be used?

  Refresh tokens have long lifetime (one year in EGI CheckIn), so they should be securely protected. If a refresh token
  is given (together with client ID and client secret), an access token will be generated on the fly.

  Access tokens have short lifetime (one hour in EGI CheckIn), so they have lower security constraints. However, they
  have to be refreshed frequently, that may be inconvenient for users. In shared environment, e.g. VMs in Cloud,
  access tokens should be used instead of refreshed tokens. In secured environment (private machines), refresh tokens
  may be permanently specified via environment variables *CHECKIN_REFRESH_TOKEN*, *CHECKIN_CLIENT_ID*,
  *CHECKIN_CLIENT_SECRET*; so users don't have to specify them at every execution.





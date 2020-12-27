import json
import os
from io import StringIO

import click
import sys
import openstackclient.shell

from fedcloudclient.checkin import get_access_token
from fedcloudclient.sites import find_endpoint_and_project_id, list_sites

DEFAULT_PROTOCOL = "openid"
DEFAULT_AUTH_TYPE = "v3oidcaccesstoken"
DEFAULT_IDENTITY_PROVIDER = "egi.eu"


# Full version of fedcloud_openstack() function, including support
# for other identity providers

def fedcloud_openstack_full(
        checkin_access_token,
        checkin_protocol,
        checkin_auth_type,
        checkin_identity_provider,
        site,
        vo,
        openstack_command,
        json_output=True
):
    """
    Calling openstack client with full options specified
    :param checkin_access_token:
    :param checkin_protocol:
    :param checkin_auth_type:
    :param checkin_identity_provider:
    :param site:
    :param vo:
    :param openstack_command:
    :param json_output:
    :return:
    """

    endpoint, project_id = find_endpoint_and_project_id(site, vo)
    if endpoint is None:
        return 1, ("VO %s not found on site %s" % (vo, site))

    options = ("--os-auth-url", endpoint,
               "--os-auth-type", checkin_auth_type,
               "--os-protocol", checkin_protocol,
               "--os-identity-provider", checkin_identity_provider,
               "--os-access-token", checkin_access_token
               )

    if vo:
        options = options + ("--os-project-id", project_id)

    # Output JSON format is useful for further machine processing
    if json_output:
        options = options + ("--format", "json")

    # Redirecting stdout and stderr from openstack client
    # to result and error string
    old_stdout = sys.stdout
    result = StringIO()
    sys.stdout = result

    old_stderr = sys.stderr
    error = StringIO()
    sys.stderr = error

    # Calling openstack client
    error_code = openstackclient.shell.main(openstack_command + options)

    sys.stdout = old_stdout
    sys.stderr = old_stderr

    if error_code == 0:
        if json_output:
            # Test if openstack command ignore JSON format option
            try:
                json_object = json.loads(result.getvalue())
                return error_code, json_object
            except ValueError as e:
                return error_code, result.getvalue()
        else:
            return error_code, result.getvalue()
    else:
        # If error code != 0, return error message instead of result
        return error_code, error.getvalue()


# Simplified version of fedcloud_openstack() function using
# default EGI setting for identity provider and protocols

def fedcloud_openstack(
        checkin_access_token,
        site,
        vo,
        openstack_command,
        json_format=True
):
    """
    Call openstack client with default options for EGI Checkin
    :param checkin_access_token:
    :param site:
    :param vo:
    :param openstack_command:
    :param json_format:
    :return:
    """

    return fedcloud_openstack_full(
        checkin_access_token,
        DEFAULT_PROTOCOL,
        DEFAULT_AUTH_TYPE,
        DEFAULT_IDENTITY_PROVIDER,
        site,
        vo,
        openstack_command,
        json_format
    )


@click.command(context_settings={"ignore_unknown_options": True})
@click.option(
    "--checkin-client-id",
    help="Check-in client id",
    default=lambda: os.environ.get("CHECKIN_CLIENT_ID", None),
)
@click.option(
    "--checkin-client-secret",
    help="Check-in client secret",
    default=lambda: os.environ.get("CHECKIN_CLIENT_SECRET", None),
)
@click.option(
    "--checkin-refresh-token",
    help="Check-in refresh token",
    default=lambda: os.environ.get("CHECKIN_REFRESH_TOKEN", None),
)
@click.option(
    "--checkin-access-token",
    help="Check-in access token",
    default=lambda: os.environ.get("CHECKIN_ACCESS_TOKEN", None),
)
@click.option(
    "--checkin-url",
    help="Check-in OIDC URL",
    required=True,
    default=lambda: os.environ.get("CHECKIN_OIDC_URL", "https://aai.egi.eu/oidc"),
)
@click.option(
    "--site",
    help="Name of the site",
    required=True,
    default=lambda: os.environ.get("EGI_SITE", None),
)
@click.option(
    "--vo",
    help="Name of the VO",
    default=lambda: os.environ.get("EGI_VO", None),
)
@click.argument(
    "openstack_command",
    nargs=-1
)
def openstack(
        checkin_client_id,
        checkin_client_secret,
        checkin_refresh_token,
        checkin_access_token,
        checkin_url,
        site,
        vo,
        openstack_command
):
    """
    CLI function for calling openstack client
    """

    access_token = get_access_token(checkin_access_token,
                                    checkin_refresh_token,
                                    checkin_client_id,
                                    checkin_client_secret,
                                    checkin_url)

    if site == "ALL_SITES":
        sites = list_sites()
    else:
        sites = [site]
    for current_site in sites:
        error_code, result = fedcloud_openstack(
            access_token,
            current_site,
            vo,
            openstack_command,
            False  # No JSON output in shell mode
        )
        print("Site: %s, VO: %s" % (current_site, vo))
        if error_code != 0:
            print("Error code: ", error_code)
            print("Error message: ", result)
        else:
            print(result)

import json
import os
from distutils.spawn import find_executable

import click
import openstackclient.shell
import subprocess

from fedcloudclient.checkin import get_access_token
from fedcloudclient.sites import find_endpoint_and_project_id, list_sites

DEFAULT_PROTOCOL = "openid"
DEFAULT_AUTH_TYPE = "v3oidcaccesstoken"
DEFAULT_IDENTITY_PROVIDER = "egi.eu"

OPENSTACK_CLIENT = "openstack"


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
    Calling openstack client with full options specified, including support
    for other identity providers and protocols

    :param checkin_access_token: Checkin access token. Passed to openstack client as --os-access-token
    :param checkin_protocol: Checkin protocol (openid, oidc). Passed to openstack client as --os-protocol
    :param checkin_auth_type: Checkin authentication type (v3oidcaccesstoken). Passed to openstack client as --os-auth-type
    :param checkin_identity_provider: Checkin identity provider in mapping (egi.eu). Passed to openstack client as --os-identity-provider
    :param site: site ID in GOCDB
    :param vo: VO name
    :param openstack_command: Openstack command in tuple, e.g. ("image", "list", "--long")
    :param json_output: if result is JSON object or string. Default:True

    :return: error code, result or error message
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

    # Calling openstack client as subprocess, caching stdout/stderr
    completed = subprocess.run((OPENSTACK_CLIENT,) + openstack_command + options, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    error_code = completed.returncode
    error_message = completed.stderr.decode('utf-8')
    result_str = completed.stdout.decode('utf-8')

    if error_code == 0:
        if json_output:
            # Test if openstack command ignore JSON format option
            try:
                json_object = json.loads(result_str)
                return error_code, json_object
            except ValueError as e:
                return error_code, result_str
        else:
            return error_code, result_str
    else:
        # If error code != 0, return error message instead of result
        return error_code, error_message


def fedcloud_openstack(
        checkin_access_token,
        site,
        vo,
        openstack_command,
        json_output=True
):
    """
    Simplified version of fedcloud_openstack_full() function using
    default EGI setting for identity provider and protocols
    Call openstack client with default options for EGI Checkin

    :param checkin_access_token: Checkin access token. Passed to openstack client as --os-access-token
    :param site: site ID in GOCDB
    :param vo: VO name
    :param openstack_command: Openstack command in tuple, e.g. ("image", "list", "--long")
    :param json_output: if result is JSON object or string. Default:True

    :return: error code, result or error message
    """

    return fedcloud_openstack_full(
        checkin_access_token,
        DEFAULT_PROTOCOL,
        DEFAULT_AUTH_TYPE,
        DEFAULT_IDENTITY_PROVIDER,
        site,
        vo,
        openstack_command,
        json_output
    )


def check_openstack_client_installation():
    """
    Check if openstack command-line client is installed and available via $PATH

    :return: True if available
    """

    return find_executable(OPENSTACK_CLIENT) is not None


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
    Calling openstack client with access token, site ID, VO name and openstack command
    """

    if not check_openstack_client_installation():
        print("Openstack client \"openstack\" does not exist")
        print("Please check if your openstack client installation is available via $PATH")
        exit(1)

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
        print("Site: %s, VO: %s" % (current_site, vo))
        error_code, result = fedcloud_openstack(
            access_token,
            current_site,
            vo,
            openstack_command,
            False  # No JSON output in shell mode
        )
        if error_code != 0:
            print("Error code: ", error_code)
            print("Error message: ", result)
        else:
            print(result)

import json
import os
from urllib.request import urlopen

import click
import yaml

site_info_files = [
    "https://raw.githubusercontent.com/EGI-Foundation/fedcloud-catchall-operations/master/sites/100IT.yaml",
    "https://raw.githubusercontent.com/EGI-Foundation/fedcloud-catchall-operations/master/sites/BIFI.yaml",
    "https://raw.githubusercontent.com/EGI-Foundation/fedcloud-catchall-operations/master/sites/CESGA.yaml",
    "https://raw.githubusercontent.com/EGI-Foundation/fedcloud-catchall-operations/master/sites/CESNET-MCC.yaml",
    "https://raw.githubusercontent.com/EGI-Foundation/fedcloud-catchall-operations/master/sites/CETA-GRID.yaml",
    "https://raw.githubusercontent.com/EGI-Foundation/fedcloud-catchall-operations/master/sites/CLOUDIFIN.yaml",
    "https://raw.githubusercontent.com/EGI-Foundation/fedcloud-catchall-operations/master/sites/CYFRONET-CLOUD.yaml",
    "https://raw.githubusercontent.com/EGI-Foundation/fedcloud-catchall-operations/master/sites/DESY-HH.yaml",
    'https://raw.githubusercontent.com/EGI-Foundation/fedcloud-catchall-operations/master/sites/IFCA-LCG2.yaml',
    "https://raw.githubusercontent.com/EGI-Foundation/fedcloud-catchall-operations/master/sites/IISAS-FedCloud-cloud.yaml",
    "https://raw.githubusercontent.com/EGI-Foundation/fedcloud-catchall-operations/master/sites/IISAS-GPUCloud.yaml",
    "https://raw.githubusercontent.com/EGI-Foundation/fedcloud-catchall-operations/master/sites/IN2P3-IRES.yaml",
    "https://raw.githubusercontent.com/EGI-Foundation/fedcloud-catchall-operations/master/sites/INFN-CATANIA-STACK.yaml",
    "https://raw.githubusercontent.com/EGI-Foundation/fedcloud-catchall-operations/master/sites/INFN-PADOVA-STACK.yaml",
    "https://raw.githubusercontent.com/EGI-Foundation/fedcloud-catchall-operations/master/sites/Kharkov-KIPT-LCG2.yaml",
    "https://raw.githubusercontent.com/EGI-Foundation/fedcloud-catchall-operations/master/sites/NCG-INGRID-PT.yaml",
    "https://raw.githubusercontent.com/EGI-Foundation/fedcloud-catchall-operations/master/sites/RECAS-BARI.yaml",
    "https://raw.githubusercontent.com/EGI-Foundation/fedcloud-catchall-operations/master/sites/SCAI.yaml",
    "https://raw.githubusercontent.com/EGI-Foundation/fedcloud-catchall-operations/master/sites/TR-FC1-ULAKBIM.yaml",
    "https://raw.githubusercontent.com/EGI-Foundation/fedcloud-catchall-operations/master/sites/UA-BITP.yaml",
    "https://raw.githubusercontent.com/EGI-Foundation/fedcloud-catchall-operations/master/sites/UNIV-LILLE.yaml",
    "https://raw.githubusercontent.com/EGI-Foundation/fedcloud-catchall-operations/master/sites/fedcloud.srce.hr.yaml",
]

site_info_data = []


def read_site_info():
    """
    Read site info from files in site_info_files to site_info_data
    :return: None
    """
    if len(site_info_data) > 0:
        return
    for filename in site_info_files:
        yaml_url = urlopen(filename)
        site_info = yaml.safe_load(yaml_url)
        site_info_data.append(site_info)


def find_site_data(site_name):
    """
    Return endpoint of the correspondent site
    :param site_name:
    :return: endpoint
    """
    read_site_info()

    for site_info in site_info_data:
        if site_info["gocdb"] == site_name:
            return site_info
    return None


def find_endpoint_and_project_id(site_name, vo):
    """
    Return Keystone endpoint and project ID from site name and VO
    :param site_name:
    :param vo:
    :return: endpoint, project_id
    """
    site_info = find_site_data(site_name)
    if site_info is None:
        return None, None

    # If only site name is given, return endpoint without project ID
    if vo is None:
        return site_info["endpoint"], None

    for vo_info in site_info["vos"]:
        if vo_info["name"] == vo:
            return site_info["endpoint"], vo_info["auth"]["project_id"]

    # Return None, None if VO not found
    return None, None


@click.group()
def site():
    """
    CLI site command group.  Execute "fedcloud site" to see more
    :return:
    """
    pass


@site.command()
@click.option(
    "--site",
    help="Name of the site",
    required=True,
    default=lambda: os.environ.get("EGI_SITE", None),
)
def print_site(site):
    """
    Print information about specified site
    :param site:
    :return: None
    """
    site_info = find_site_data(site)
    if site_info:
        print(json.dumps(site_info, indent=2))
    else:
        print("Site %s not found" % site)


@site.command()
@click.option(
    "--site",
    help="Name of the site",
    required=True,
    default=lambda: os.environ.get("EGI_SITE", None),
)
@click.option(
    "--vo",
    help="Name of the VO",
    required=True,
    default=lambda: os.environ.get("EGI_VO", None),
)
def print_project_id(site, vo):
    """
    CLI command for printing keystone URL and project ID of the VO on the site
    :param site:
    :param vo:
    :return:
    """
    endpoint, project_id = find_endpoint_and_project_id(site, vo)
    if endpoint:
        print(" Endpoint : %s \n Project ID : %s" % (endpoint, project_id))
    else:
        print("Site %s or VO %s not found" % (site, vo))


@site.command()
def print_all():
    """
    Print all site info
    :return:
    """
    if len(site_info_data) == 0:
        read_site_info()
    for site_info in site_info_data:
        site_info_str = json.dumps(site_info, indent=2)
        print(site_info_str)

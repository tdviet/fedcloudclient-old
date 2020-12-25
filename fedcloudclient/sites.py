import json
import os
from pathlib import Path
from urllib.request import urlopen

import click
import yaml

# Default site configs from GitHub
default_site_configs = [
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

site_config_data = []

local_config_dir = ".fedcloud-site-config/"


def read_site_config():
    """
    Read site info from files in site_info_files to site_info_data

    :return: None
    """
    if len(site_config_data) > 0:
        return
    config_dir = Path.home() / local_config_dir
    if config_dir.exists():
        read_local_site_config(config_dir)
    else:
        read_default_site_config()


def read_default_site_config():
    """
    Read default site config from GitHub

    :return:
    """
    site_config_data.clear()
    for filename in default_site_configs:
        yaml_file = urlopen(filename)
        site_info = yaml.safe_load(yaml_file)
        site_config_data.append(site_info)


def read_local_site_config(config_dir):
    """
    Read site config from local directory

    :param config_dir:
    :return:
    """
    site_config_data.clear()
    config_dir = Path(config_dir)
    for f in config_dir.glob('*.yaml'):
        yaml_file = f.open()
        site_info = yaml.safe_load(yaml_file)
        site_config_data.append(site_info)


def save_site_config(config_dir):
    """
    Save site configs to local directory. Overwrite local configs if exist

    :param config_dir: config directory
    :return:
    """
    config_dir = Path(config_dir)
    config_dir.mkdir(parents=True, exist_ok=True)
    for site_info in site_config_data:
        config_file = config_dir / (site_info["gocdb"] + ".yaml")
        with config_file.open("w", encoding="utf-8") as f:
            yaml.dump(site_info, f)


def find_site_data(site_name):
    """
    Return endpoint of the correspondent site

    :param site_name:
    :return: endpoint
    """
    read_site_config()

    for site_info in site_config_data:
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
    CLI site command group.
    """
    pass


@site.command()
@click.option(
    "--site",
    help="Name of the site",
    required=True,
    default=lambda: os.environ.get("EGI_SITE", None),
)
def show(site):
    """
    Print information about specified site
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
def show_project_id(site, vo):
    """
    CLI command for printing keystone URL and project ID of the VO on the site
    """
    endpoint, project_id = find_endpoint_and_project_id(site, vo)
    if endpoint:
        print(" Endpoint : %s \n Project ID : %s" % (endpoint, project_id))
    else:
        print("Site %s or VO %s not found" % (site, vo))


@site.command()
def show_all():
    """
    Print all site info
    """
    read_site_config()
    for site_info in site_config_data:
        site_info_str = json.dumps(site_info, indent=2)
        print(site_info_str)


@site.command()
def save_config():
    """
    Read default site configs from GigHub and save them to local folder in home directory
    Overwrite local configs if exist
    """
    read_default_site_config()
    config_dir = Path.home() / local_config_dir
    print("Saving site configs to directory %s" % config_dir)
    save_site_config(config_dir)


@site.command()
def list():
    """
    List site IDs
    """
    read_site_config()
    for site_info in site_config_data:
        print(site_info["gocdb"])

#!/usr/bin/python3
"""Automated deployment script for web_static content."""
from fabric.api import *
from datetime import datetime
from os.path import exists
from os.path import basename
from os.path import getsize


env.hosts = ["34.229.66.172", "54.82.132.21"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/school"
created_archive = None


def do_pack():
    """
    Create a compressed archive of the web_static folder.

    Returns:
        str: The file path of the created archive,
            or None if the process fails.
    """
    global created_archive
    if created_archive is not None:
        return created_archive
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = "versions/web_static_{}.tgz".format(date)
    print(f"Packing web_static to {file_name}")
    try:
        if not exists("versions"):
            if local("mkdir -p versions").failed is True:
                return None
        if local("tar -cvzf {} web_static".format(file_name)).failed is True:
            return None
        print(f"web_static packed: {file_name} -> {getsize(file_name)}Bytes")
        created_archive = file_name
        return file_name
    except Exception:
        return None


def do_deploy(archive_path):
    """
    Deploy the web_static content to remote servers.

    Args:
        archive_path (str): Path to the compressed archive to deploy.

    Returns:
        bool: True if deployment succeeds, False otherwise.

    Raises:
        Exception: If an error occurs during the deployment process.
    """
    if exists(archive_path) is False:
        return False
    file_name = basename(archive_path).split(".")[0]
    file = "/data/web_static/releases/{}/".format(file_name)
    tmp = "/tmp/{}.tgz".format(file_name)
    if exists('/data/web_static/releases'):
        local("cp {} /tmp".format(archive_path))
        local("rm -rf {}".format(file))
        local("mkdir -p {}".format(file))
        local("tar -xzf {} -C {}".format(tmp, file))
        local("rm {}".format(tmp))
        local("mv {}web_static/* {}".format(file, file))
        local("rm -rf {}web_static".format(file))
        local("rm -rf /data/web_static/current")
        local("ln -s {} /data/web_static/current".format(file))
    try:
        if put(archive_path, "/tmp/").failed is True:
            return False
        if run("mkdir -p {}".format(file)).failed is True:
            return False
        if run("tar -xzf {} -C {}".format(tmp, file)).failed is True:
            return False
        if run("rm {}".format(tmp)).failed is True:
            return False
        if run("mv {}web_static/* {}".format(file, file)).failed is True:
            return False
        if run("rm -rf {}web_static".format(file)).failed is True:
            return False
        if run("rm -rf /data/web_static/current").failed is True:
            return False
        if (
            run("ln -s {} /data/web_static/current".format(file)).failed
            is True
        ):
            return False
        print("New version deployed!")
        return True
    except Exception:
        return False


def deploy():
    """
    Automate the process of creating and deploying web_static content.

    Returns:
        bool: True if the deployment process succeeds, False otherwise.
    """
    file_path = do_pack()
    if not exists(file_path):
        return False
    rsl = do_deploy(file_path)
    return rsl

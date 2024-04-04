#!/usr/bin/python3
"""
Fabric script based on the file 2-do_deploy_web_static.py that creates and
distributes an archive to the web servers

execute: fab -f 3-deploy_web_static.py deploy -i ~/.ssh/school -u ubuntu
"""
import os.path
import time
from fabric.api import local
from fabric.operations import env, put, run

env.hosts = ["34.229.66.172", "54.82.132.21"]


def do_pack():
    """Generate an tgz archive from web_static folder"""
    try:
        local("mkdir -p versions")
        local("tar -cvzf versions/web_static_{}.tgz web_static/".
              format(time.strftime("%Y%m%d%H%M%S")))
        return ("versions/web_static_{}.tgz".format(time.
                                                    strftime("%Y%m%d%H%M%S")))
    except:
        return None


def do_deploy(archive_path):
    """Distribute an archive to web servers"""
    if (os.path.isfile(archive_path) is False):
        return False

    try:
        file = archive_path.split("/")[-1]
        folder = ("/data/web_static/releases/" + file.split(".")[0])
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(folder))
        run("sudo tar -xzf /tmp/{} -C {}".format(file, folder))
        run("sudo rm /tmp/{}".format(file))
        run("sudo mv {}/web_static/* {}/".format(folder, folder))
        run("sudo rm -rf {}/web_static".format(folder))
        run('sudo rm -rf /data/web_static/current')
        run("sudo ln -s {} /data/web_static/current".format(folder))
        print("Deployment done")
        return True
    except:
        return False


def deploy():
    """Create and distributes an archive to web servers"""
    try:
        path = do_pack()
        return do_deploy(path)
    except:
        return False

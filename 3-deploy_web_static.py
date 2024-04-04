#!/usr/bin/python3
'''
Module contains a fab script to generates a .tgz archive from the contents
of the web_static
'''
from fabric.api import local, env, put, run
import os
import time

env.user = 'ubuntu'
env.hosts = ["34.229.66.172", "54.82.132.21"]


def do_pack():
    '''
    A function that generaees a .tgx archive from the web_static folder
    '''
    if not os.path.exists('versions'):
        os.makedirs('versions')

    filename = time.strftime("%Y%m%d%H%M%S")
    fullpath = "versions/web_static_{}.tgz".format(filename)
    try:
        local("tar -cvzf {} web_static".format(fullpath))
        return fullpath
    except:
        return None


def do_deploy(archive_path):
    '''
    Distributes an archive to my webservers
    '''
    if not os.path.isfile(archive_path):
        return False

    # Upload the archive to the server
    put(archive_path, '/tmp/')

    # Create directory where we will extract the file to
    file_name = archive_path.split('/')[-1]  # Get file name
    dir_path = '/data/web_static/releases/{}'.format(file_name.split('.')[0])
    run('mkdir -p {}'.format(dir_path))

    # Uncompress the archive to the folder
    server_archive_path = '/tmp/' + file_name  # Path of archive in server
    run('tar -xzf {} -C {}'.format(server_archive_path, dir_path))

    # Delete the archive from the web server
    run('rm -rf {}'.format(server_archive_path))

    # Delete the symbolic link
    run('rm -rf /data/web_static/current')

    # Move the files from web_static to web_static_<number>
    run('mv {}/web_static/* {}'.format(dir_path, dir_path))
    run('rm -rf {}/web_static'.format(dir_path))

    # Create a new symbolic link
    run('ln -s {} /data/web_static/current'.format(dir_path))

    return True


def deploy():
    '''
    Deploys my webstatic files to my servers
    '''
    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)

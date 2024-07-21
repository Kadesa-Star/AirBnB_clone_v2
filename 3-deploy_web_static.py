#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to web servers.

Usage:
    fab -f 3-deploy_web_static.py deploy -i ~/.ssh/id_rsa -u ubuntu
"""

from fabric.api import env, local, put, run
from datetime import datetime
from os.path import exists, isdir

# Define your server IPs
env.hosts = ['100.25.202.17', '34.207.62.126']


def do_pack():
    """Generates a .tgz archive of the web_static directory."""
    try:
        # Create the versions directory if it doesn't exist
        if not isdir("versions"):
            local("mkdir versions")
        # Create the archive filename with a timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_name = "versions/web_static_{}.tgz".format(timestamp)
        # Create the archive
        local("tar -cvzf {} web_static".format(archive_name))
        return archive_name
    except Exception as e:
        print(f"Error in do_pack: {e}")
        return None


def do_deploy(archive_path):
    """Distributes an archive to the web servers."""
    if not exists(archive_path):
        return False
    try:
        # Extract filename and path information
        file_name = archive_path.split("/")[-1]
        base_name = file_name.split(".")[0]
        release_path = "/data/web_static/releases/"
        # Upload the archive to the remote server
        put(archive_path, '/tmp/')
        # Create the release directory and extract the archive
        run('mkdir -p {}{}/'.format(release_path, base_name))
        run('tar -xzf /tmp/{} -C {}{}/'.format(
            file_name, release_path, base_name)
            )
        # Clean up temporary files
        run('rm /tmp/{}'.format(file_name))
        # Move the contents and update symbolic link
        run('mv {0}{1}/web_static/* {0}{1}/'.format(release_path, base_name))
        run('rm -rf {}{}/web_static'.format(release_path, base_name))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(
            release_path, base_name)
            )
        return True
    except Exception as e:
        print(f"Error in do_deploy: {e}")
        return False


def deploy():
    """Creates and distributes an archive to the web servers."""
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)

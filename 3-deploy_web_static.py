#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to the web servers.

Usage: fab -f 3-deploy_web_static.py deploy -i ~/.ssh/id_rsa -u ubuntu
"""

from fabric.api import env, local, put, run
from datetime import datetime
from os.path import exists, isdir

# Define the list of servers
env.hosts = ['100.25.202.17', '34.207.62.126']


def do_pack():
    """Generate a .tgz archive from the web_static directory."""
    try:
        # Create a timestamp for the archive file name
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        # Ensure the versions directory exists
        if not isdir("versions"):
            local("mkdir versions")
        # Define the archive file name and path
        archive_file = "versions/web_static_{}.tgz".format(timestamp)
        # Create the archive
        local("tar -cvzf {} web_static".format(archive_file))
        return archive_file
    except Exception as e:
        print(f"Error creating archive: {e}")
        return None


def do_deploy(archive_path):
    """Distribute an archive to the web servers."""
    if not exists(archive_path):
        return False
    try:
        # Extract the file name and name without extension
        file_name = archive_path.split("/")[-1]
        base_name = file_name.split(".")[0]
        # Define the remote path
        remote_path = "/data/web_static/releases/"
        # Upload the archive to the remote server
        put(archive_path, '/tmp/')
        # Create the directory on the remote server
        run('mkdir -p {}{}/'.format(remote_path, base_name))
        # Extract the archive
        run('tar -xzf /tmp/{} -C {}{}/'.format(
            file_name, remote_path, base_name)
            )
        # Remove the archive from the remote server
        run('rm /tmp/{}'.format(file_name))
        # Move files and clean up
        run('mv {0}{1}/web_static/* {0}{1}/'.format(remote_path, base_name))
        run('rm -rf {}{}/web_static'.format(remote_path, base_name))
        run('rm -rf /data/web_static/current')
        # Create a symlink to the new release
        run('ln -s {}{}/ /data/web_static/current'.format(
            remote_path, base_name)
            )
        return True
    except Exception as e:
        print(f"Error deploying archive: {e}")
        return False


def deploy():
    """Create and distribute an archive to the web servers."""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)

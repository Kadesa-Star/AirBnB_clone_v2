#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""

from fabric.api import put, run, env
from os.path import exists

# Define the hosts (web servers)
env.hosts = ['100.25.202.17', '34.207.62.126']


def do_deploy(archive_path):
    """Distributes an archive to the web servers."""
    if not exists(archive_path):
        return False

    try:
        # Extract the file name and name without extension
        file_name = archive_path.split("/")[-1]
        base_name = file_name.split(".")[0]
        remote_path = "/data/web_static/releases/"

        # Upload the archive to the /tmp/ directory
        put(archive_path, '/tmp/')

        # Create the release directory
        release_dir = '{}{}/'.format(remote_path, base_name)
        run('mkdir -p {}'.format(release_dir))

        # Uncompress the archive
        run('tar -xzf /tmp/{} -C {}'.format(file_name, release_dir))

        # Remove the archive from the server
        run('rm /tmp/{}'.format(file_name))

        # Move files to the correct location
        run('mv {0}{1}/web_static/* {0}{1}/'.format(remote_path, base_name))

        # Remove old symlink and create a new one
        run('rm -rf {}{}/web_static'.format(remote_path, base_name))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(
            remote_path, base_name)
            )

        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

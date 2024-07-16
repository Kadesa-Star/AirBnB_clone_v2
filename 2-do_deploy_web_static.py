#!/usr/bin/python3
"""
Fabric script to deploy an archive to
web servers based on the file 1-pack_web_static.py.
"""

from fabric.api import put, run, env
from os.path import exists

# Define the host servers where deployment will occur
env.hosts = ['54.89.109.87', '100.25.190.21']


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers and deploys it.

    Args:
        archive_path (str): Path to the archive file to deploy.

    Returns:
        bool: True if deployment was successful, False otherwise.
    """
    # Check if the archive file exists
    if exists(archive_path) is False:
        return False

    try:
        # Extract necessary information from the archive path
        file_name = archive_path.split("/")[-1]
        no_extension = file_name.split(".")[0]
        release_path = "/data/web_static/releases/"

        # Upload the archive to /tmp/ directory on the web server
        put(archive_path, '/tmp/')

        # Create the directory for the new release
        run('mkdir -p {}{}/'.format(release_path, no_extension))

        # Uncompress the archive into the new release directory
        run('tar -xzf /tmp/{} -C {}{}/'
            .format(file_name, release_path, no_extension))

        # Remove the uploaded archive from /tmp/
        run('rm /tmp/{}'.format(file_name))

        # Move contents of the extracted folder to its parent directory
        run('mv {0}{1}/web_static/* {0}{1}/'
            .format(release_path, no_extension))

        # Clean up by removing the now empty web_static folder
        run('rm -rf {}{}/web_static'.format(release_path, no_extension))

        # Remove existing /data/web_static/current symbolic link
        run('rm -rf /data/web_static/current')

        # Create new symbolic link /data/web_static
        # /current linked to the new version
        run('ln -s {}{}/ /data/web_static/current'
            .format(release_path, no_extension))

        return True  # Deployment successful

    except Exception as e:
        print("Deployment failed:", str(e))
        return False  # Deployment failed

#!/usr/bin/python3
"""
Fabric script to deploy an archive to web servers.
"""

import os
from fabric.api import env, put, run

# Define the host servers for deployment
env.hosts = ['100.25.202.17', '34.207.62.126']


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers and deploys it.

    Args:
        archive_path (str): Path to the archive file to deploy.

    Returns:
        bool: True if deployment was successful, False otherwise.
    """
    if not os.path.isfile(archive_path):
        return False

    file_name = os.path.basename(archive_path)
    name = file_name.split(".")[0]
    release_path = f"/data/web_static/releases/{name}"

    # Upload the archive to the /tmp/ directory on the server
    if put(archive_path, f"/tmp/{file_name}").failed:
        return False

    # Create the directory for the new release
    if run(f"mkdir -p {release_path}").failed:
        return False

    # Uncompress the archive into the new release directory
    if run(f"tar -xzf /tmp/{file_name} -C {release_path}").failed:
        return False

    # Remove the uploaded archive from /tmp/
    if run(f"rm /tmp/{file_name}").failed:
        return False

    # Move contents of the extracted folder to its parent directory
    if run(f"mv {release_path}/web_static/* {release_path}/").failed:
        return False

    # Clean up by removing the now empty web_static folder
    if run(f"rm -rf {release_path}/web_static").failed:
        return False

    # Remove existing /data/web_static/current symbolic link
    if run("rm -rf /data/web_static/current").failed:
        return False

    # Create new symbolic link /data/web_static/current linked to the new version
    if run(f"ln -s {release_path} /data/web_static/current").failed:
        return False

    return True

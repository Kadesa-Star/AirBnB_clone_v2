#!/usr/bin/python3
"""
Fabric script to distribute an archive to web servers.
"""

import os
from fabric import Connection

# Define the host servers for deployment
env_hosts = ['100.25.202.17', '34.207.62.126']  # Your server IPs


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

    for host in env_hosts:
        conn = Connection(host=host, user='ubuntu')
        # Added user 'ubuntu'
        try:
            # Upload the archive to the /tmp/ directory on the server
            conn.put(archive_path, f"/tmp/{file_name}")

            # Create the directory for the new release
            conn.run(f"mkdir -p {release_path}")

            # Uncompress the archive into the new release directory
            conn.run(f"tar -xzf /tmp/{file_name} -C {release_path}")

            # Remove the uploaded archive from /tmp/
            conn.run(f"rm /tmp/{file_name}")

            # Move contents of the extracted folder to its parent directory
            conn.run(f"mv {release_path}/web_static/* {release_path}/")

            # Clean up by removing the now empty web_static folder
            conn.run(f"rm -rf {release_path}/web_static")

            # Remove existing /data/web_static/current symbolic link
            conn.run("rm -rf /data/web_static/current")

            # Create new symbolic link /data/web_static/current
            # linked to the new version
            conn.run(f"ln -s {release_path} /data/web_static/current")

            print(f"New version deployed on {host}!")
        except Exception as e:
            print(f"Deployment failed on {host}: {e}")
            return False

    return True

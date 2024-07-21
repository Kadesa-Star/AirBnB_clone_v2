#!/usr/bin/python3
"""
Fabric script to distribute an archive to web servers.
"""

from fabric import task, Connection
from fabric.transfer import Transfer
from os.path import exists

env_hosts = ['100.25.202.17', '34.207.62.126']


def do_deploy(ctx, archive_path):
    """
    Distributes an archive to the web servers.
    Args:
        ctx (Context): Fabric's context object.
        archive_path (str): Path to the archive file to deploy.

    Returns:
        bool: True if deployment was successful, False otherwise.
    """
    if not exists(archive_path):
        return False

    file_name = archive_path.split("/")[-1]
    file_base = file_name.split(".")[0]
    release_path = f"/data/web_static/releases/{file_base}"

    for host in env_hosts:
        conn = Connection(
                host=host,
                user=ctx.user,
                connect_kwargs={
                    "key_filename": ctx.key_filename
                    }
                )
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

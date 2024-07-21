#!/usr/bin/python3
"""
Fabric script to distribute an archive to web servers.
"""

from fabric import Connection, task
from os.path import exists

# Define the server IP addresses
HOSTS = ['100.25.202.17', '34.207.62.126']

@task
def do_deploy(c, archive_path):
    """Distributes an archive to the web servers."""
    if not exists(archive_path):
        return False
    
    try:
        # Extract filename and no extension
        file_name = archive_path.split("/")[-1]
        no_ext = file_name.split(".")[0]
        path = "/data/web_static/releases/"

        # Upload the archive
        c.put(archive_path, '/tmp/')

        # Create release directory and uncompress the archive
        c.run(f'mkdir -p {path}{no_ext}/')
        c.run(f'tar -xzf /tmp/{file_name} -C {path}{no_ext}/')

        # Clean up temporary archive
        c.run(f'rm /tmp/{file_name}')

        # Move files and clean up old release
        c.run(f'mv {path}{no_ext}/web_static/* {path}{no_ext}/')
        c.run(f'rm -rf {path}{no_ext}/web_static')

        # Update symbolic link
        c.run(f'rm -rf /data/web_static/current')
        c.run(f'ln -s {path}{no_ext}/ /data/web_static/current')

        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

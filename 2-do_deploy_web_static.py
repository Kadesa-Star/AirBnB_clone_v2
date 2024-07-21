#!/usr/bin/python3
"""
Fabric script to deploy an archive to web servers.
"""

from fabric.api import put, run, env
from os.path import exists

# Define the list of web servers
env.hosts = ['100.25.202.17', '34.207.62.126']


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers.

    Args:
        archive_path (str): The local path to the archive file.

    Returns:
        bool: True if deployment is successful, False otherwise.
    """
    # Check if the archive exists
    if not exists(archive_path):
        return False
    
    try:
        # Extract filename and name without extension
        file_name = archive_path.split("/")[-1]
        file_name_no_ext = file_name.split(".")[0]
        remote_path = "/data/web_static/releases/"
        
        # Upload the archive to the server
        put(archive_path, '/tmp/')
        
        # Create the directory for the release
        run(f'mkdir -p {remote_path}{file_name_no_ext}/')
        
        # Uncompress the archive
        run(f'tar -xzf /tmp/{file_name} -C {remote_path}{file_name_no_ext}/')
        
        # Remove the archive from the server
        run(f'rm /tmp/{file_name}')
        
        # Move the files from the archive directory
        run(f'mv {remote_path}{file_name_no_ext}/web_static/* {remote_path}{file_name_no_ext}/')
        
        # Remove the old web_static directory
        run(f'rm -rf {remote_path}{file_name_no_ext}/web_static')
        
        # Remove the current symbolic link
        run('rm -rf /data/web_static/current')
        
        # Create a new symbolic link to the new release
        run(f'ln -s {remote_path}{file_name_no_ext}/ /data/web_static/current')
        
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

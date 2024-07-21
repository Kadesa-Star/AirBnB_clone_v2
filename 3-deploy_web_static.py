#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to the web servers.

Execute: fab -f 3-deploy_web_static.py deploy -i ~/.ssh/id_rsa -u ubuntu
"""

from fabric.api import env, local, put, run
from datetime import datetime
from os.path import exists, isdir


# Define the hosts with your specific servers
env.hosts = ['100.25.202.17', '34.207.62.126']


def do_pack():
    """Generates a tgz archive."""
    try:
        # Generate a timestamped filename
        date = datetime.now().strftime("%Y%m%d%H%M%S")

        # Ensure the versions directory exists
        if not isdir("versions"):
            local("mkdir versions")

        # Define the file name
        file_name = "versions/web_static_{}.tgz".format(date)

        # Create the archive
        local("tar -cvzf {} web_static".format(file_name))
        return file_name

    except Exception as e:
        print(f"Error creating archive: {e}")
        return None


def do_deploy(archive_path):
    """Distributes an archive to the web servers."""
    if not exists(archive_path):
        return False

    try:
        # Extract the file name and name without extension
        file_name = archive_path.split("/")[-1]
        base_name = file_name.split(".")[0]
        remote_path = "/data/web_static/releases/"

        # Upload the archive to the remote server
        put(archive_path, '/tmp/')

        # Create the release directory
        release_dir = '{}{}/'.format(remote_path, base_name)
        run('mkdir -p {}'.format(release_dir))

        # Extract the archive
        tar_command = (
            'tar -xzf /tmp/{} -C {}'.format(file_name, release_dir)
        )
        run(tar_command)

        # Remove the archive from the remote server
        run('rm /tmp/{}'.format(file_name))

        # Move files to the correct location
        move_command = (
            'mv {0}{1}/web_static/* {0}{1}/'.format(remote_path, base_name)
        )
        run(move_command)

        # Remove old symlink and create a new one
        run('rm -rf {}{}/web_static'.format(remote_path, base_name))
        run('rm -rf /data/web_static/current')

        symlink_command = (
            'ln -s {}{}/ /data/web_static/current'.format(
                remote_path, base_name)
        )
        run(symlink_command)

        return True

    except Exception as e:
        print(f"Error deploying archive: {e}")
        return False


def deploy():
    """Creates and distributes an archive to the web servers."""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)

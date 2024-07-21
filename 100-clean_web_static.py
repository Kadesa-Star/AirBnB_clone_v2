#!/usr/bin/python3
"""
Deletes out-of-date archives.
Usage:
    fab -f 100-clean_web_static.py
    do_clean:number=2 -i my_ssh_private_key -u ubuntu
"""

import os
from fabric.api import env, local, run, lcd, cd

# Define the hosts (web servers)
env.hosts = ['100.25.202.17', '34.207.62.126']


def do_clean(number=0):
    """Delete old archives, keeping only a specified number of recent ones.
    Args:
        number (int): The number of archives to keep.
        If number is 0 or 1, only the most recent archive is kept. If
        number is 2, the most recent and the second-most recent archives
        are kept, and so forth.
    """
    number = 1 if int(number) == 0 else int(number)

    # Local archive cleanup
    local_archives = sorted(os.listdir("versions"))
    if len(local_archives) > number:
        outdated_local_archives = local_archives[:-number]
        with lcd("versions"):
            for archive in outdated_local_archives:
                local("rm ./{}".format(archive))

    # Remote archive cleanup
    for host in env.hosts:
        with cd("/data/web_static/releases"):
            remote_archives = run("ls -tr").split()
            remote_archives = [
                    a for a in remote_archives if "web_static_" in a
                    ]
            if len(remote_archives) > number:
                outdated_remote_archives = remote_archives[:-number]
                for archive in outdated_remote_archives:
                    run("rm -rf ./{}".format(archive))

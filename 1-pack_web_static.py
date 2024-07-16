#!/usr/bin/python3
"""
Fabric script to generate a .tgz archive from the contents of the web_static folder
"""

from fabric.api import *
from datetime import datetime

def do_pack():
    """
    Packs the web_static folder into a .tgz archive

    Returns:
        str: Archive path if successful, None if there's an error
    """
    try:
        # Create the current time string in the required format
        now = datetime.now()
        time_str = now.strftime("%Y%m%d%H%M%S")

        # Create the versions folder if it doesn't exist
        local("mkdir -p versions")

        # Create the archive path
        archive_path = "versions/web_static_{}.tgz".format(time_str)

        # Compress the web_static folder into the archive_path
        local("tar -cvzf {} web_static".format(archive_path))

        # Return the archive path if successful
        return archive_path
    except Exception as e:
        print(f"Error packing: {e}")
        return None

if __name__ == "__main__":
    do_pack()

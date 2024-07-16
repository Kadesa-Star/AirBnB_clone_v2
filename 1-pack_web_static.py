#!/usr/bin/python3
# Fabfile to generate a .tgz archive from the contents of web_static.
import os.path
from datetime import datetime
from fabric.api import local


def do_pack():
    """Create a tar gzipped archive of the web_static directory."""
    # Generate timestamp for the archive filename
    dt = datetime.utcnow()
    archive_name = "web_static_{}{}{}{}{}{}.tgz".format(dt.year,
                                                        dt.month,
                                                        dt.day,
                                                        dt.hour,
                                                        dt.minute,
                                                        dt.second)
    # Create the directory 'versions' if it doesn't exist
    if not os.path.exists("versions"):
        local("mkdir -p versions")

    # Create the .tgz archive
    archive_path = "versions/{}".format(archive_name)
    result = local("tar -cvzf {} web_static".format(archive_path))

    # Return the path to the archive if successful, otherwise None
    if result.failed:
        return None
    else:
        return archive_path

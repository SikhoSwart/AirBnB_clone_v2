#!/usr/bin/python3
"""
a script (based on the file 2-do_deploy_web_static.py) that creates and
distributes an archive to web servers
"""
import os.path
from fabric.api import *
from fabric.operations import run, put
from datetime import datetime


env.hosts = ['3.227.217.150', '3.95.27.202']
env.user = "ubuntu"


def deploy():
    """creates and distributes an archive to your web servers
    """
    archive_path = do_pack()
    if archive_path is None:
        print("Failed to create archive from web_static")
        return False
    return do_deploy(archive_path)


def do_pack():
    """ generates a .tgz archive from the contents of the web_static
    """
    if not os.path.isdir("versions"):
        os.mkdir("versions")
    cur_time = datetime.now()
    output = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        cur_time.year,
        cur_time.month,
        cur_time.day,
        cur_time.hour,
        cur_time.minute,
        cur_time.second
    )
    try:
        print("Packing web_static to {}".format(output))
        local("tar -cvzf {} web_static".format(output))
        archize_size = os.stat(output).st_size
        print("web_static packed: {} -> {} Bytes".format(output, archize_size))
    except Exception:
        output = None
    return output


def do_deploy(archive_path):
    """distributes an archive to your web servers.
    """
    if not os.path.exists(archive_path):
        return False
    file_name = os.path.basename(archive_path)
    folder_name = file_name.replace(".tgz", "")
    folder_path = "/data/web_static/releases/{}/".format(folder_name)
    success = False

    try:
        put(archive_path, "/tmp/{}".format(file_name))
        run("mkdir -p {}".format(folder_path))
        run("tar -xzf /tmp/{} -C {}".format(file_name, folder_path))
        run("rm -rf /tmp/{}".format(file_name))
        run("mv {}web_static/* {}".format(folder_path, folder_path))
        run("rm -rf {}web_static".format(folder_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(folder_path))
        print('New version deployed!')
        success = True

    except Exception:
        success = False
        print("Could not deploy")
    return success

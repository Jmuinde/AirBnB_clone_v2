#!/usr/bin/env python3
# Fabric script to distribute arhcived files to the web servers 
# using the function deploy

from datetime import datetime
from fabric.api import env, local, put, run, runs_once
import os

# List of host server IP addresses
env.hosts = ["162.243.160.35", "142.93.192.52"]


def do_pack():
	"""Function to archive static files."""
	if not os.path.isdir("versions"):
		os.mkdir("versions")
	current_time = datetime.now()
	output = "versions/web_static_{}{}{}{}{}{}.tgz".format(
		current_time.year,
		current_time.month,
		current_time.day,
		current_time.hour,
		current_time.minute,
		current_time.second
	)

	try:
		print("Archiving web_static to {}".format(output))
		local("tar -cvzf {} web_static".format(output))
		archize_size = os.stat(output).st_size
		print("web_static packed: {} -> {} Bytes".format(output, archize_size))
		return output
	except Exception as er:
		print("An error aoccured:", er)
		output = None
	return output


def do_deploy(archive_path):
	"""Deploys the compressed static files to the host servers.
	Args:
		archive_path (str): The path to the archived static files.
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
	return success

def deploy():
	"""Archives and deploys the static files to the host servers.
	"""
	archive_path = do_pack()
	return do_deploy(archive_path) if archive_path else False

def do_clean(number=0):
    """Deletes out-of-date archives of the static files.
    Args:
        number: The number of archives to keep.
    """
    archives = os.listdir('versions/')
    archives.sort(reverse=True)
    start = int(number)
    if not start:
        start += 1
    if start < len(archives):
        archives = archives[start:]
    else:
        archives = []
    for archive in archives:
        os.unlink('versions/{}'.format(archive))
    cmd_parts = [
        "rm -rf $(",
        "find /data/web_static/releases/ -maxdepth 1 -type d -iregex",
        " '/data/web_static/releases/web_static_.*'",
        " | sort -r | tr '\\n' ' ' | cut -d ' ' -f{}-)".format(start + 1)
    ]
    run(''.join(cmd_parts))


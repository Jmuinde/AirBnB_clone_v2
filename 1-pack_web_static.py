#!/usr/bin/env python3
# A Fabric script that compresses files

from datetime import datetime
from fabric.api import local, runs_once
import os
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

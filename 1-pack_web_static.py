#!/usr/bin/env python3
# A Fabric script that compresses files

from fabric import task # because I am using fabric 2.x
from datetime import datetime
from fabric import Collection 
import os

# Flag to control if task has already run
do_pack_executed = False


@task
def do_pack(c):
	"""Function to archive static files."""
	global do_pack_executed # Access the global flag
	if do_pack_executed:
		print("do_pack function already executed. Skipping.")
		return None
	do_pack_executed = True # Mark function as executed 

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
		c.local("tar -cvzf {} web_static".format(output))
		archize_size = os.stat(output).st_size
		print("web_static packed: {} -> {} Bytes".format(output, archize_size))
		return output
	except Exception as er:
		print("An error aoccured:" er)
		output = None
	return output
		
#Create a collection for tasks 
ns = Collection ()
ns.add_task(do_pack)

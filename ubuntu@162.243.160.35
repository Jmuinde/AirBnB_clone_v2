#!/usr/bin/env bash
# Script to set up the webservers for the deployment of web_static

server_config="server {
		listen 80 default_server;
		listen [::]:80 default_server;
		
		server_name _;
		index index.html index.htm;
		error_page 404 /404.html;
		add_header X-served-By \$hostname;

		location / {
				root /var/www/html/;
				try_files \$uri \$uri/ =404;
		}
		
		location /hbnb_static/ {
				alias /data/web_static/current/;
				try_files \$uri \$uri/ =404;
		}

	location = /404.html {
				root /var/www/error/;
				internal;
		}
	}"

home_page="<!DOCTYPE html>
<html lang='en'>
	<head>
		<title>Home - AirBnB Clone</title>
	</head>
	<body>
		<h1>Welcome to AirBnB!</h1>
	</body>
</html>
"
# check if nginx is intstalled and install

if [ "$(which nginx | grep -c nginx)" -eq 0 ]; then 
	apt-get update
	apt-get -y install nginx
fi

# Create necessary directories
mkdir -p /data/web_static/releases/test /data/web_static/shared /var/www/html /var/www/error
chmod -R 755 /var/www

# Add basic HTML files
echo 'happy holidays' > /var/www/html/index.html
echo '<h1>404 Not Found </h1>' > /var/www/error/404.html
echo -e "$home_page" > /data/web_static/releases/test/index.html

# Create / replace the symbolic link
[ -d /data/web_static/current ] && rm -rf /data/web_static/current
ln -sf /data/web_static/releases/test/ /data/web_static/current

# Assign ownership to ubuntu user AND group
chown -hR ubuntu:ubuntu /data

# back up existing Nginx configuration
if [ -f /etc/nginx/sites-available/default ]; then
    cp /etc/nginx/sites-available/default /etc/nginx/sites-available/default.bak
fi
# Update Nginx configuration 
bash -c "echo -e '$server_config' > /etc/nginx/sites-available/default"
ln -sf '/etc/nginx/sites-available/default' '/etc/nginx/sites-enabled/default'

# Validate Nginx configuration
if ! nginx -t; then
    echo "Nginx configuration is invalid. Restoring backup..."
    cp /etc/nginx/sites-available/default.bak /etc/nginx/sites-available/default
    exit 1
fi

# Restart or start Nginx
if [ "$(pgrep -c nginx)" -le 0 ]; then 
	service nginx start
else
	service nginx restart
fi

exit 0

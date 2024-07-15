#!/usr/bin/env bash
# Sets up a web server for deployment of web_static within an Ubuntu container.

# Update package lists and install nginx
apt-get update
apt-get install -y nginx

# Create necessary directories
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# Create a fake HTML file for testing
echo "Holberton School" > /data/web_static/releases/test/index.html

# Create symbolic link with correct ownership
rm -rf /data/web_static/current  # Remove existing symlink if any
ln -sf /data/web_static/releases/test/ /data/web_static/current

# Change ownership and group recursively
chown -R root /data/
chgrp -R root /data/

# Configure Nginx to serve /data/web_static/current/ to hbnb_static
printf %s "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By \$HOSTNAME;
    root   /var/www/html;
    index  index.html index.htm;

    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }

    location /redirect_me {
        return 301 http://cuberule.com/;
    }

    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}" > /etc/nginx/sites-available/default

# Restart Nginx to apply changes
service nginx restart

exit 0

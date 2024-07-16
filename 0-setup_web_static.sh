#!/usr/bin/env bash
# Script that sets up web servers for the deployment of web_static

# Update package lists and install Nginx if not already installed
sudo apt-get update
sudo apt-get -y install nginx

# Allow Nginx HTTP through the firewall
sudo ufw allow 'Nginx HTTP'

# Create necessary directories if they don't already exist
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create a fake HTML file with simple content to test Nginx configuration
sudo tee /data/web_static/releases/test/index.html > /dev/null << EOF
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
EOF

# Create a symbolic link, forcefully if it exists
sudo ln -sfn /data/web_static/releases/test/ /data/web_static/current

# Give ownership of /data/ to the ubuntu user and group recursively
sudo chown -R ubuntu:ubuntu /data/

# Remove any existing location block for /hbnb_static to avoid duplicates
sudo sed -i '/location \/hbnb_static {/,/}/d' /etc/nginx/sites-available/default

# Update Nginx configuration to serve the content
sudo sed -i '/listen 80 default_server/a location /hbnb_static { alias /data/web_static/current/; }' /etc/nginx/sites-available/default

# Test Nginx configuration and restart the service if the test is successful
sudo nginx -t && sudo service nginx restart

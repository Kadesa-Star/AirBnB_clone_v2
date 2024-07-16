#!/usr/bin/env bash

# Update apt-get and install nginx
apt-get update
apt-get install -y nginx

# Create necessary directories if they don't exist
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# Create the complete HTML file with the specified format
cat <<EOF > /data/web_static/releases/test/index.html
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
EOF

# Create a symbolic link if it doesn't exist or recreate if it does
if [ ! -e /data/web_static/current ]; then
    ln -s /data/web_static/releases/test/ /data/web_static/current
else
    rm -rf /data/web_static/current
    ln -s /data/web_static/releases/test/ /data/web_static/current
fi

# Change ownership of /data/ directory recursively to ubuntu user and group
chown -R ubuntu:ubuntu /data/

# Configure nginx to serve the content
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

# Restart nginx service
service nginx restart

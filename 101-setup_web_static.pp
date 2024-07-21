# This manifest configures the Nginx web server to deploy web_static.

# Define the Nginx configuration as a variable
$nginx_config = @("EOF")
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By ${hostname};
    root   /var/www/html;
    index  index.html index.htm;
    
    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }
    
    location /redirect_me {
        return 301 https://th3-gr00t.tk;
    }
    
    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}
EOF

# Ensure Nginx is installed
package { 'nginx':
  ensure => 'installed',
  provider => 'apt',
} ->

# Create the necessary directories for the web static content
file { '/data':
  ensure => 'directory',
} ->

file { '/data/web_static':
  ensure => 'directory',
} ->

file { '/data/web_static/releases':
  ensure => 'directory',
} ->

file { '/data/web_static/releases/test':
  ensure => 'directory',
} ->

file { '/data/web_static/shared':
  ensure => 'directory',
} ->

# Add a sample HTML file for testing
file { '/data/web_static/releases/test/index.html':
  ensure  => 'file',
  content => "Holberton School Puppet\n",
} ->

# Create a symbolic link to the latest release
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
} ->

# Set the correct ownership for the /data directory
exec { 'set_permissions':
  command => 'chown -R ubuntu:ubuntu /data/',
  path    => ['/usr/bin', '/usr/local/bin', '/bin'],
} ->

# Ensure the /var/www/html directory and its contents are present
file { '/var/www':
  ensure => 'directory',
} ->

file { '/var/www/html':
  ensure => 'directory',
} ->

file { '/var/www/html/index.html':
  ensure  => 'file',
  content => "Holberton School Nginx\n",
} ->

file { '/var/www/html/404.html':
  ensure  => 'file',
  content => "Ceci n'est pas une page\n",
} ->

# Deploy the Nginx configuration file
file { '/etc/nginx/sites-available/default':
  ensure  => 'file',
  content => $nginx_config,
} ->

# Reload Nginx to apply the new configuration
exec { 'reload_nginx':
  command => '/usr/sbin/nginx -s reload',
  path    => '/usr/sbin',
  notify  => Service['nginx'],
}

# Ensure the Nginx service is running
service { 'nginx':
  ensure => 'running',
  enable => true,
}

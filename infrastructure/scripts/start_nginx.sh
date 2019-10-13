# Install nginx
yum install -y epel-release
yum install -y nginx 

# Copy nginx.conf
cp /home/django/educa/educa/config/nginx.conf /etc/nginx/nginx.conf
    
# enable and start nginx.conf
systemctl enable nginx
systemctl start nginx

# redirect domain account to local /etc/hosts
echo "127.0.0.1 educaproject.com" >> /etc/hosts
echo "127.0.0.1 www.educaproject.com" >> /etc/hosts


cp /home/django/educa/educa/infrastructure/scripts/uwsgi_django /usr/bin
cp /home/django/educa/educa/infrastructure/scripts/systemd-uwsgi /etc/systemd/system/uwsgi.service
systemctl start uwsgi 

# Link CSS for admin pages
cd /home/django/educa/educa/courses/static ; ln -s /home/django/educa/venv/lib/python2.7/site-packages/django/contrib/admin/static/admin admin
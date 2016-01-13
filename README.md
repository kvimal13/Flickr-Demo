# Flickr-Demo
A Sample project to Showcase Flickr Images: Python(cherrypy/redis)
Process to setup Flickr-Demo

cd /var/www

sudo chmod 777 -R /var/www

git clone https://github.com/kvimal13/Flickr-Demo.git

cd /var/www/Flickr-Demo

# Setup Virtualenv

virtualenv env

#install necessary packages

env/bin/pip install cherrypy

env/bin/pip install redis

env/pip install jinja2


# Run the project

env/bin/python application/controller.py


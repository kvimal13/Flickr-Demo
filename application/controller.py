# -*- coding: utf-8 -*-
import cherrypy
import redis
import requests
import json
import config
import jinja2
import os

viewLoader   = jinja2.FileSystemLoader(os.path.join(config.path, 'public', 'resource','templates'))
env = jinja2.Environment(loader=viewLoader)

redis_server = redis.StrictRedis()

class FlickrImages(object):
    @cherrypy.expose
    def index(self):
		response = requests.get(url='https://api.flickr.com/services/feeds/photos_public.gne?format=json&nojsoncallback=1')
		raw_json = response.content
		raw_json = unicode(raw_json, 'utf-8')
		res = json.loads("%s"%raw_json)
		for items in res['items']:
			redis_server.set('image_url',items['media']['m'])
		image = redis_server.get('image_url')
		tmpl = env.get_template('flickr.html')
		return tmpl.render(value=image)


def get_app(config=None):
    cherrypy.tree.mount(FlickrImages(), '/',config=config)
    return cherrypy.tree


def start():
    get_app()
    cherrypy.engine.signals.subscribe()
    cherrypy.engine.start()
    cherrypy.engine.block()

if __name__ == '__main__':
	cherrypy.config.update({'server.socket_port': 8090})
	start()



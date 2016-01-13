# -*- encoding: utf-8 -*-
import cherrypy
import redis
import requests
import json
import config as conf
import jinja2
import os
import threading
import datetime

viewLoader   = jinja2.FileSystemLoader(os.path.join(conf.path, 'public', 'resource','templates'))
env = jinja2.Environment(loader=viewLoader)

redis_server = redis.StrictRedis()

class FlickrImages(object):
	@cherrypy.expose
	def index(self):
		data = {}
		threading.Timer(0.25, index).start()
		print '-------------------------------'
		response = requests.get(url='https://api.flickr.com/services/feeds/photos_public.gne?format=json&nojsoncallback=1')
		raw_json = response.content
		raw_json = unicode(raw_json, 'utf-8')
		res = json.loads("%s"%raw_json)
		for items in res['items']:
			redis_server.set(items['title'],items['media']['m'])
		for title in redis_server.scan_iter():
			data[unicode(title, 'utf-8')] = redis_server.get(title)
		tmpl = env.get_template('flickr.html')
		return tmpl.render(value=data)




def start():
	cherrypy.tree.mount(FlickrImages(), '/',{'/': {
             'tools.staticdir.on': True,
             'tools.staticdir.dir': os.path.abspath(os.path.dirname(__file__))
         }
	})
	cherrypy.engine.signals.subscribe()
	cherrypy.engine.start()
	cherrypy.engine.block()


if __name__ == '__main__':
	cherrypy.config.update({'server.socket_port': 8090})
	start()



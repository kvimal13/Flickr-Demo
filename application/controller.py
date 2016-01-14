# -*- encoding: utf-8 -*-
import cherrypy
import redis
import requests
import json
import jinja2
import os
import threading
import datetime

path   = os.path.abspath(os.path.dirname(__file__))
viewLoader   = jinja2.FileSystemLoader(os.path.join(path, 'public', 'resource','templates'))
env = jinja2.Environment(loader=viewLoader)


redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
redis_server = redis.from_url(redis_url)

class FlickrImages(object):
	@cherrypy.expose
	def index(self):
		data = {}
		threading.Timer(300, self.index).start()
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
	cherrypy.config.update({'server.socket_host': '0.0.0.0','server.socket_port': int(os.environ.get('PORT', 5000))})
	start()



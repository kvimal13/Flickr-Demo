import os


path   = os.path.abspath(os.path.dirname(__file__))

config = {
         '/': {
             'tools.staticdir.on': True,
             'tools.staticdir.dir': './public/resource'
         }
}
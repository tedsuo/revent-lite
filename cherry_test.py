import cherrypy

class Foo:
	def bar(self):
		return 'Yo'
	bar.exposed = True
	def index(self):
		return 'lalala'
	index.exposed = True

cherrypy.quickstart(Foo())

# RESTFUL interface for google spreadsheet-as-a-database

import cherrypy
import gdata.spreadsheet.text_db
import json
import urllib
from string import Template
from datetime import datetime 

# set up logging
cherrypy.log.screen = True
cherrypy.log.access_file = '/home/avalos/public_new/everywhere/access.log'
cherrypy.log.error_file = '/home/avalos/public_new/everywhere/error.log'

# geocode gets lat,long for an address
def geocode(address):
	url = 'http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false' % address
	f = urllib.urlopen(url)
	location = json.loads(f.read())['results'][0]['geometry']['location']
        cherrypy.log(repr( location ))
        return location

# used to format data for geocoder
address_template = Template('$address, $city, $zip')

# load html into memory
with open('form.html','r') as f:
	form_html = f.read()

# setup database connection and Events model
client 	= gdata.spreadsheet.text_db.DatabaseClient(username='ted@radicaldesigns.org',password='ryogas12')
db      = client.GetDatabases(spreadsheet_key='0AgCuKXHzk8-UdC15RWZKNmF6dU56R3hiUW1EV2p2QUE')[0]
Events 	= db.GetTables(name='Sheet1')[0]

# Google Spreadsheet Controller
class EventController:

	def index(self,name,address,city,zip,description,host_name,email,phone):
                cherrypy.log.error('started request')
		location = geocode(address=address_template.substitute(address=address, city=city, zip=zip))
		record = { 
			'timestamp':str(datetime.now()),
			'title': name, 
			'address': address, 
			'city': city, 
			'zip': zip, 
			'description': description, 
			'eventhostcontactemailaddress': email, 
			'eventhostphonenumber': phone, 
#			'eventstarttime': start_time, 
#			"eventendtime" : end_time, 
			'lat': str(location['lat']), 
			'long': str(location['lng']) 
		}
                cherrypy.log.error(str(record))
		result = Events.AddRecord(record)
                cherrypy.log.error(str(result))
                cherrypy.log.error('ended request')
		return 'success'
	index.exposed = True

	def fetch(self):
		return str(Events.GetRecords())

# start the server
cherrypy.quickstart(EventController())

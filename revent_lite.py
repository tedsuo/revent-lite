# RESTFUL interface for google spreadsheet-as-a-database

import cherrypy
import gdata.spreadsheet.text_db
import json
import urllib
from string import Template
from datetime import datetime 
 
# geocode gets lat,long for an address
def geocode(address):
	url = 'http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false' % address
	print url
	f = urllib.urlopen(url)
	return json.loads(f.read())['results'][0]['geometry']['location']

# used to format data for geocoder
address_template = Template('$address, $city, $zip')

# load html into memory
with open('form.html','r') as f:
	form_html = f.read()

# setup database connection and Events model
client 	= gdata.spreadsheet.text_db.DatabaseClient(username='ted@radicaldesigns.org',password='ryogas12')
db 		= client.GetDatabases(spreadsheet_key='0Audib9Y4DZuxdDMtX3Voa0ZGcldzSzR4TGwxLWtWMUE')[0]
Events 	= db.GetTables(name='events')[0]

# RESTFUL Google Spreadsheet Controller
class EventController:
	def index(self):
		return form_html
	index.exposed = True

	def create(self,name,address,city,zip,description,host_name,email,phone,start_time,end_time):
		location = geocode(address=address_template.substitute(address=address, city=city, zip=zip))
		Events.AddRecord({ 
			'timestamp':str(datetime.now()),
			'nameofevent': name, 
			'streetaddressorintersectionofevent': address, 
			'city': city, 
			'zip': zip, 
			'eventdescription': description, 
			'eventhostcontactemailaddress': email, 
			'eventhostphonenumber': phone, 
			'eventstarttime': start_time, 
			"eventendtime" : end_time, 
			'lat': str(location['lat']), 
			'long': str(location['lng']) 
		})
		return 'success'
	create.exposed = True

# start the server
cherrypy.quickstart(EventController())

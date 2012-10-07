import urllib,urllib2
import json
from flask import Flask,jsonify,request
app = Flask(__name__)

@app.route('/photos')
def get_photos():
	user = ''
	tags = ''
	if 'user' in request.args:
		user = request.args['user']
	if 'tags' in request.args:
		tags = request.args['tags']
	if user is '' and tags is '':
		return 'error: must supply either user, tags, or both'
	if user is '':
		return jsonify(get_photos(tags,''))
	else:
		id = get_user_id(user)
		return jsonify(get_photos(tags, id))
		
def get_user_id(user):
	url = 'http://api.flickr.com/services/rest/'
	params = { 'api_key' :'d99a583f0b168b27152d3b67bf01b0dc',
	'username': user,
	'method': 'flickr.people.findByUsername',
	'format': 'json',
	'nojsoncallback': 1 }
	id = call_api(url,params)['user']['id']
	return id

def get_photos(tags, id):
	url = 'http://api.flickr.com/services/rest/'
	params = { 'api_key' :'d99a583f0b168b27152d3b67bf01b0dc',
	'content_type':1,
	'user_id': id,
	'extras':'tags',
	'method': 'flickr.photos.search',
	'tags' : tags,
	'sort': 'date-posted-desc',
	'media': 'photos',
	'format': 'json',
	'per_page': 20,
	'nojsoncallback': 1 }
	photo_list = call_api(url,params)
	return photo_list

def call_api(url,params):
	data = urllib.urlencode(params)
	req = urllib2.Request(url, data)
	result = json.loads(urllib2.urlopen(req).read())   #returns a Python dict of the JSON from Flickr
	return result

if __name__ == '__main__':
	app.debug = True
	app.run()
	

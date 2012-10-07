import urllib,urllib2,os
import json
from flask import Flask,jsonify,request
app = Flask(__name__)

#routes -------------------------------------------------------------------
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
	urls = get_photo_urls(user,tags)
	return(urls)
	
@app.route('/shorten')
def get_short_url():
	long_url = ''
	if 'url' in request.args:
		long_url = request.args['url']
	else:
		return 'error: must supply url to shorten'
	url = 'https://api-ssl.bitly.com/v3/shorten'
	u = 'iolabproject'
	k = 'R_27b34f4c5bb5326cb5c0d2e482adeb19'
	params = {
	'longUrl': long_url,
	'login': u,
	'apiKey': k,
	'domain':'bit.ly'
	}
	shorturl = call_api(url,params)['data']['url']
	return shorturl
	
#helper functons -------------------------------------------------------------------
def get_photo_urls(user,tags):
	photo_list = []
	ids = []
	result_list = []
	if user is '':
		photo_list = get_photo_list(tags,'')
	else:
		id = get_user_id(user)
		photo_list = get_photo_list(tags, id)
	for photo in photo_list['photos']['photo']:
		ids.append(photo['id'])
	for pid in ids:
		item = get_photo_byid(pid)['sizes']['size'][0]
		thumbnail_url = item['url']
		full_url = item['source']
		result_list += [{'full':full_url,'thumb':thumbnail_url}]
	return(json.dumps(result_list))
	
def get_user_id(user):
	url = 'http://api.flickr.com/services/rest/'
	params = { 'api_key' :'d99a583f0b168b27152d3b67bf01b0dc',
	'username': user,
	'method': 'flickr.people.findByUsername',
	'format': 'json',
	'nojsoncallback': 1 }
	id = call_api(url,params)['user']['id']
	return id
		
def get_photo_list(tags, id):
	url = 'http://api.flickr.com/services/rest/'
	params = { 'api_key' :'d99a583f0b168b27152d3b67bf01b0dc',
	'content_type':1,
	'user_id': id,
	'extras':'tags',
	'method': 'flickr.photos.search',
	'sort': 'date-posted-desc',
	'media': 'photos',
	'format': 'json',
	'per_page': 20,
	'nojsoncallback': 1 }
	photo_list = call_api(url,params)
	return photo_list

def get_photo_byid(id):
	url = 'http://api.flickr.com/services/rest/'
	params = { 'api_key' :'d99a583f0b168b27152d3b67bf01b0dc',
	'method' : 'flickr.photos.getSizes',
	'photo_id' : id,
	'format' : "json",
	'nojsoncallback' : 1 }
	photo = call_api(url,params)
	return photo
	
def call_api(url,params):
	data = urllib.urlencode(params)
	req = urllib2.Request(url, data)
	result = json.loads(urllib2.urlopen(req).read())   #returns a Python dict of the JSON from Flickr
	return result

if __name__ == '__main__':
        app.debug = True
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port)
	

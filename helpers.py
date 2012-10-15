import os
import re
import urllib
import urllib2
import json

from collections import Counter

FLICKR_URL = 'http://api.flickr.com/services/rest/'
FLICKR_KEY = 'd99a583f0b168b27152d3b67bf01b0dc'


def get_hashtags_from_search(results):
    """Extract hashtags from Tweepy search results and tally the number
    of times each tag occurs
    """
    hashtags = []
    for result in results:
        hashtags += re.findall(r"#(\w+)", result.text)
    hashtag_counts = Counter(hashtags).most_common(15)
    # Reverse list because items will be prepended in ascending order
    hashtag_counts.reverse()
    return json.dumps(hashtag_counts)

def get_photo_urls(user, tags):
    photo_list = []
    ids = []
    result_list = []

    if user is '':
        photo_list = get_photo_list(tags, '')
    else:
        id = get_user_id(user)
        photo_list = get_photo_list(tags, id)

    for photo in photo_list['photos']['photo']:
        ids.append(photo['id'])

    for pid in ids:
        pdata = get_photo_byid(pid)['sizes']['size']
        thumbnail_url = pdata[0]['source']
        full_url = pdata[len(pdata)-1]['url']
        result_list += [{'full': full_url, 'thumb': thumbnail_url}]

    return(json.dumps(result_list))

def get_user_id(user):
    params = {
        'api_key' : FLICKR_KEY,
        'username': user,
        'method': 'flickr.people.findByUsername',
        'format': 'json',
        'nojsoncallback': 1,
    }
    return call_api(FLICKR_URL, params)['user']['id']

def get_photo_list(tags, id):
    params = {
        'api_key': FLICKR_KEY,
        'content_type': 1,
        'user_id': id,
        'tags': tags,
        'method': 'flickr.photos.search',
        'sort': 'date-posted-desc',
        'media': 'photos',
        'format': 'json',
        'per_page': 20,
        'nojsoncallback': 1,
    }
    return call_api(FLICKR_URL, params)

def get_photo_byid(id):
    params = {
        'api_key' : FLICKR_KEY,
        'method': 'flickr.photos.getSizes',
        'photo_id': id,
        'format': 'json',
        'nojsoncallback': 1,
    }
    return call_api(FLICKR_URL, params)

def call_api(url, params):
    data = urllib.urlencode(params)
    req = urllib2.Request(url, data)
    # Returns a Python dict of the JSON from Flickr
    return json.loads(urllib2.urlopen(req).read())

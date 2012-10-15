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
    tags = ','.join(tags.split())
    if user is '':
        photo_list = get_photo_list(tags, '')
    else:
        id = get_user_id(user)
        photo_list = get_photo_list(tags, id)

    result_list = []
    for photo in photo_list['photos']['photo']:
        result_list += [{
            'id': photo['id'],
            'full': 'http://flic.kr/p/' + base58encode(int(photo['id'])),
            'thumb': photo.get('url_sq')
        }]

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
        'tag_mode': 'all',
        'method': 'flickr.photos.search',
        'sort': 'relevance',
        'media': 'photos',
        'format': 'json',
        'per_page': 20,
        'nojsoncallback': 1,
        'extras': 'url_b,url_sq',
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

def base58encode(num):
    """ Returns num in a base58-encoded string for Flickr shortner"""

    alphabet = '123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'
    base_count = len(alphabet)

    encode = ''
    if (num < 0):
        return ''

    while (num >= base_count):
        mod = num % base_count
        encode = alphabet[mod] + encode
        num = num / base_count

    if (num):
        encode = alphabet[num] + encode

    return encode
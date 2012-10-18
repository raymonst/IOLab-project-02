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
    tags = tags.split(' ')
    for tag in tags:
        if is_stopword(tag):
            tags.remove(tag)
    tags = ','.join(tags)
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

def is_stopword(tag):
    stopwords = ["a","able","about","across","after","all","almost","also","am",
        "among","an","and","any","are","as","at","be","because","been","but","by",
        "can","cannot","could","dear","did","do","does","either","else","ever",
        "every","for","from","get","got","had","has","have","he","her","hers","him",
        "his","how","however","i","if","in","into","is","it","its","just","least",
        "let","like","likely","may","me","might","most","must","my","neither","no",
        "nor","not","of","off","often","on","only","or","other","our","own","rather",
        "said","say","says","she","should","since","so","some","than","that","the",
        "their","them","then","there","these","they","this","tis","to","too","twas",
        "us","wants","was","we","were","what","when","where","which","while","who",
        "whom","why","will","with","would","yet","you","your" ]

    if tag in stopwords:
        return True
    return False

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

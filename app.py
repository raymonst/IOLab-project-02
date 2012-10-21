import os
import json
import tweepy
from flask import (
    Flask,
    Response,
    session,
    redirect,
    abort,
    url_for,
    escape,
    request,
    render_template,
)
from sentiment import sentiment
from helpers import get_photo_urls, call_api, get_hashtags_from_search

app = Flask(__name__)
app.secret_key = '9gb1krq^_@s&*)qz03^jcfl4w+tle660s$z1#mtemu5b(m=$fudn##@'

TWITTER_CONSUMER_TOKEN = os.environ.get('TWITTER_CONSUMER_TOKEN')
TWITTER_CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
TWITTER_CALLBACK_URL = 'verify'
TWITTER_NUM_RESULTS = 100
TWITTER_PAGES_TO_POLL = 2

BITLY_URL = 'https://api-ssl.bitly.com/v3/shorten'
BITLY_USER = 'iolabproject'
BITLY_KEY = 'R_27b34f4c5bb5326cb5c0d2e482adeb19'


@app.route("/")
def request_token():
    auth = tweepy.OAuthHandler(
        TWITTER_CONSUMER_TOKEN,
        TWITTER_CONSUMER_SECRET,
        os.path.join(request.url_root, TWITTER_CALLBACK_URL)
    )

    try:
        redirect_url = auth.get_authorization_url()
        session['request_token'] = (
            auth.request_token.key,
            auth.request_token.secret,
        )
    except tweepy.TweepError, e:
        return abort(401)

    return redirect(redirect_url)

@app.route('/main')
def main():
    auth = session.get('auth')
    if not auth:
        return request_token()

    api = tweepy.API(auth)
    return render_template('index.html',
        user=api.me(),
        tweets=api.user_timeline(count=10),
    )

@app.route('/tweets')
def tweets():
    auth = session.get('auth')
    api = tweepy.API(auth)

    return render_template('tweets.html',
        tweets=api.user_timeline(),
    )

@app.route("/verify")
def request_access():
    verifier = request.args.get('oauth_verifier')

    auth = tweepy.OAuthHandler(
        TWITTER_CONSUMER_TOKEN,
        TWITTER_CONSUMER_SECRET,
    )

    request_key, request_secret = session.pop('request_token')
    auth.set_request_token(request_key, request_secret)
    try:
        auth.get_access_token(verifier)
    except tweepy.TweepError:
        return abort(401)

    session['auth'] = auth
    return redirect(url_for('main'))

@app.route("/update_status")
def update_status():
    auth = session.get('auth')
    api = tweepy.API(auth)

    tweet_id = None
    status = None
    success = False
    try:
        response = api.update_status(request.args.get('m'))
        tweet_id = response.id_str
    except tweepy.TweepError, e:
        status = str(e)
    else:
        success = True

    # tweet_id can be used in the following URL to fetch details:
    # https://api.twitter.com/1/statuses/show/257274356126863360.json
    return Response(
        response=json.dumps({
            'id': tweet_id,
            'success': success,
            'status': status,
            'username': api.me().screen_name,
        }),
        status=200,
        mimetype='application/json',
    )

@app.route("/hashtags")
def get_hashtags():
    auth = session.get('auth')
    api = tweepy.API(auth)

    query = request.args.get('q')
    latlng = request.args.get('location')

    num_results = request.args.get('num_results', TWITTER_NUM_RESULTS)

        
    results = []
    if (query):
        for i in xrange(1, TWITTER_PAGES_TO_POLL + 1):
            results += api.search(
                query,
                lang="en",
                result_type='mixed',
                rpp=num_results,
                page=i,
            )
    else:           #tweepy doesn't allow you to search without a query...but twitter does
        for i in xrange(1, TWITTER_PAGES_TO_POLL + 1):
            results += call_api('http://search.twitter.com/search.json?',
                params = { 'geocode' : '37.781157,-122.398720,1mi', 'rpp':num_results, 'page':i } 
                )['results']

    hashtags = get_hashtags_from_search(results)
    return Response(
        response=hashtags,
        status=200,
        mimetype='application/json',
    )

@app.route("/sentiment")
def get_sentiment():
    message = request.args.get('m')
    return Response(
        response=json.dumps({
            'sentiment': sentiment(message),
        }),
        status=200,
        mimetype='application/json',
    )

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

    urls = get_photo_urls(user, tags)
    return Response(
        response=urls,
        status=200,
        mimetype='application/json',
    )

@app.route('/shorten')
def get_short_url():
    long_url = ''
    if 'url' in request.args:
        long_url = request.args['url']
    else:
        return 'error: must supply url to shorten'

    params = {
        'longUrl': long_url,
        'login': BITLY_USER,
        'apiKey': BITLY_KEY,
        'domain':'bit.ly'
    }
    return call_api(BITLY_URL, params)['data']['url']

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)     # heroku
    #app.run()                               # for running locally

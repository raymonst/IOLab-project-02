import os
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
import tweepy

from helpers import get_photo_urls, call_api

app = Flask(__name__)
app.secret_key = '9gb1krq^_@s&*)qz03^jcfl4w+tle660s$z1#mtemu5b(m=$fudn##@'

TWITTER_CONSUMER_TOKEN = os.environ.get('TWITTER_CONSUMER_TOKEN')
TWITTER_CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
TWITTER_CALLBACK_URL = 'verify'

FLICKR_URL = 'http://api.flickr.com/services/rest/'
FLICKR_KEY = 'd99a583f0b168b27152d3b67bf01b0dc'

BITLY_URL = 'https://api-ssl.bitly.com/v3/shorten'
BITLY_USER = 'iolabproject'
BITLY_KEY = 'R_27b34f4c5bb5326cb5c0d2e482adeb19'


@app.route("/")
def request_token():
    print os.path.join(request.url_root, TWITTER_CALLBACK_URL)
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


@app.route('/main')
def main():
    auth = session.get('auth')
    api = tweepy.API(auth)

    return render_template('index.html',
        user=api.me(),
        tweets=api.user_timeline(),
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

    urls = get_photo_urls(user,tags)
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

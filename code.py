#!/usr/bin/env python
from bottle import route, get, post, request, abort
import bottle
import memcache
import tenjin
from tenjin.helpers import *
import redis
import url

#bottle.debug(True)


def get_latest_short_url():
    r = redis.Redis(host='localhost', port=6379)
    return r.get('last_url')

def save_url(long_url, short_url):
    assert long_url
    assert short_url

    if not long_url.startswith('http'):
        long_url = 'http://' + long_url

    r = redis.Redis(host='localhost', port=6379)

    r.set('last_url', short_url)
    r.set(short_url, long_url)
    return True

@get('/')
def index_get():
    #import pdb; pdb.set_trace()
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)
    home_get = mc.get('home_get')
    if not home_get:
        engine = tenjin.Engine()
        context = {}
        home_get = engine.render('templates/home_get.html', context)
        mc.set("home_get", home_get)
    return home_get
    #return "Hello World!"

#run(host='localhost', port=8080)
#from paste import httpserver
#httpserver.serve(bottle.default_app(), host='0.0.0.0', port=80)


@post('/')
def index_post():
    long_url = request.forms.get('long_url')
    latest_short_url = get_latest_short_url()

    if not latest_short_url:
        short_url = 'a'
        print long_url
        print short_url
        save_url(long_url, short_url)
    else:
        short_url = url.increment(latest_short_url)
        save_url(long_url, short_url)

    engine = tenjin.Engine()
    short_url = 'http://url.gennad.org/' + short_url
    context = {'short_url': short_url}
    home_post = engine.render('templates/home_post.html', context)
    return home_post

@post('/send_ajax')
def send_ajax():
    long_url = request.forms.get('long_url')
    latest_short_url = get_latest_short_url()

    if not latest_short_url:
        short_url = 'a'
        save_url(long_url, short_url)
    else:
        short_url = url.increment(latest_short_url)
        save_url(long_url, short_url)

    short_url = 'http://url.gennad.org/' + short_url
    resdict = {'short_url': short_url}
    return resdict


from bottle import static_file
@route('/static/js/:filename')
def server_static(filename):
    return static_file(filename, root='/home/gennad/urlshortener/static/js/')

from bottle import redirect
@route('/:short_url#[a-z]+#')
def redirect_user(short_url):
    r = redis.Redis(host='localhost', port=6379)
    long_url = r.get(short_url)
    if long_url:
        redirect(long_url)
    else:
        abort(404, "Not found")

from gevent import wsgi
#application = web.application(urls, globals(), autoreload=False).wsgifunc() 
wsgi.WSGIServer(('', 8088), bottle.default_app(), spawn=None).serve_forever()

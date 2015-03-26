from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import subprocess
import urllib2
import json

# Create your views here.
initial_url = "https://www.facebook.com/search/124349814392124/likers/pages-liked"
ending = {
'books':'/book/pages/intersect',
'musicians': '/musician/pages/intersect',
'companies': '/employer/pages/intersect',
'movies': '/movie/pages/intersect',
'games': '/game/pages/intersect',
'all': ''
}

class Listing:
    def __init__(self, link, image_url, thumbnail, title):
        self.link = link
        self.image_url = image_url
        self.thumbnail = thumbnail
        self.title = title

def url_to_username(url):
    username = url[url.rfind('/')+1:]
    return username

def username_to_id(username):
    print(username)
    p_id = ""
    try:
        f = urllib2.urlopen("http://graph.facebook.com/"+username)
	unpacked = json.loads(f.read())
        p_id = unpacked['id']
    except urllib2.HTTPError as e:
        print(e)
    return p_id

def generate_listings(raw):
    listings = []
    for i in raw:
        link = "/explore/"+i+"/all"
        image_url = "http://graph.facebook.com/"+i+"/picture?type=large"
        thumbnail = "http://graph.facebook.com/"+i+"/picture?type=square"
        try:
            f = urllib2.urlopen("http://graph.facebook.com/"+i)
            unpacked = json.loads(f.read())
            title = unpacked['name'].strip()
            listing = Listing(link, image_url, thumbnail, title)
            listings.append(listing)
        except urllib2.HTTPError as e:
            print(e)
    return listings

def s_index(req):
    raw_listings = subprocess.check_output(['casperjs', 'fastscrape.js', initial_url]).splitlines()
    listings = generate_listings(raw_listings)
    search = generate_listings(['MHacksHackathon'])[0]
    return render(req, 'explore.djt.html', {'listings': listings, 'search': search, 'selected': 'all'})

def s_explore(req):
    stype = req.path[req.path.rfind('/')+1:]
    rest = req.path[:req.path.rfind('/')]
    username = rest[rest.rfind('/')+1:]
    print(rest, username)
    p_id = username_to_id(username) 
    url = "https://www.facebook.com/search/"+p_id+"/likers/pages-liked"+ending[stype]
    print(url)
    try:
        raw_listings = subprocess.check_output(['casperjs', 'fastscrape.js', url]).splitlines()
    except subprocess.CalledProcessError as e:
        return render(req, 'context-defined.djt.html', {'title': 'Error', 'content': 'Invalid URL', }) 
    listings = generate_listings(raw_listings)
    search = generate_listings([username])[0]
    return render(req, 'explore.djt.html', {'listings': listings, 'search': search, 'selected': stype})

def s_search_helper(req):
    query = req.GET['q']
    type = req.GET['type']
    graph_url = 'https://www.facebook.com/search/str/'+query+'/pages-named'
    raw_listing = subprocess.check_output(['casperjs', 'fastscrape.js', graph_url]).splitlines()[0]
    return HttpResponseRedirect("/explore/"+raw_listing+"/"+type)

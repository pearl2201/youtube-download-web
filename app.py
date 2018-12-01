# -*- coding: utf-8 -*-

import os

import google.oauth2.credentials
import re
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from flask import (Flask,Blueprint, flash, g, redirect,render_template,request,session,url_for,abort,jsonify)
import youtube_dl
import json
import httplib2
import apiclient
from operator import itemgetter 
from functools import cmp_to_key

app = Flask(__name__)
# Note: A secret key is included in the sample so that it works, but if you
# use this code in your application please replace this with a truly secret
# key. See http://flask.pocoo.org/docs/0.12/quickstart/#sessions.
app.secret_key = 'AIzaSyC778FuABmYJfUhPwa-HaY-U7xXV9ZJZnM'

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

ydl_opts = {
    'ext': 'mp4',
    'format':'bestvideo'
 
}


def sortkeypicker(keynames):
    negate = set()
    for i, k in enumerate(keynames):
        if k[:1] == '-':
            keynames[i] = k[1:]
            negate.add(k[1:])
    def getit(adict):
       composite = [adict[k] for k in keynames]
       for i, (k, v) in enumerate(zip(keynames, composite)):
           if k in negate:
               composite[i] = -v
       return composite
    return getit

def build_request(http, *args, **kwargs):
	new_http = httplib2.Http()
	return apiclient.http.HttpRequest(new_http, *args, **kwargs)

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
client = build(API_SERVICE_NAME, API_VERSION, developerKey='AIzaSyC778FuABmYJfUhPwa-HaY-U7xXV9ZJZnM',requestBuilder=build_request)

def parse_response_youtube(data):
	with open('result_youtube.json','w') as f:
		f.write(json.dumps(data,indent=4, sort_keys=True))
		f.close()
	ret = []
	for item in data["items"]:
		
		if item["id"]["kind"] == "youtube#video" and item["snippet"]["liveBroadcastContent"] == "none":
			ret.append({
				'videoId':item["id"]["videoId"],
				'name':item['snippet']['title'],
				'thumb':item["snippet"]["thumbnails"]["medium"]["url"]

	})
		
	return ret

@app.before_request
def before_request():
    if True:
        print ("HEADERS", request.headers)
        print ("REQ_path", request.path)
        print ("ARGS",request.args)
        print ("DATA",request.data)
        print ("FORM",request.form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
@app.route('/index/')
def index():
	return render_template('index.html')

@app.route('/api/search/',methods=('GET','POST'))
def api_search():
	print (request.data)
	q = request.json["query"]
	match = re.search(r"youtube\.com/.*v=([^&]*)", q)
	if match:
		id = match.group(1)
	else:
		id = q
	if not id:
		return '',200

	try:

		response = client.search().list(
			part='snippet',
			maxResults=25,
			q=id
			).execute()
		
	except Exception as e:
		print (e)
		return jsonify({})
	return jsonify(parse_response_youtube(dict(**response)))

@app.route('/search/', methods=('GET','POST'))
def get_search_page():

	if not request.args.get("ytsearch-text"):
		return render_template('search.html',search_text=q)

	q = request.args["ytsearch-text"]

	match = re.search(r"youtube\.com/.*v=([^&]*)", q)

	if match:
		id = match.group(1)
	else:
		id = q

	if not id:
		return render_template('search.html',search_text=q)

	try:

		response = client.search().list(
			part='snippet',
			maxResults=25,
			q=id
			).execute()
		
	except Exception as e:
		print (e)
		return jsonify({})
	print (parse_response_youtube(dict(**response)))
	return render_template('search.html',search_text=q,data=parse_response_youtube(dict(**response)))


def searchStr(keyword):
	response = client.search().list(
		part='snippet',
		maxResults=25,
		q=keyword
		).execute()
	return jsonify(**response)

@app.route('/video/',methods=('POST',))
def redirect_video():
	
	return jsonify({'url':url_for('video',id=request.json["id"])})

@app.route('/video/<id>/')
def video(id):
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ret = ydl.extract_info('https://www.youtube.com/watch?v=%s' %id,download=False,process=True)
	data = {
    	'title':ret["title"],
    	'formats': [],
    	'id':id
    }
	formats = []
	for format in ret["formats"]:
		if format.get("filesize"):
			temp = {
    		'size': "%.2f" %(int(format["filesize"])/(1024*1024)),
    		'ext': format["ext"],
    		'url': format["url"],
    		'audio': "audio only" in format["format"]

    		}	
			formats.append(temp)

	sorted_formats = sorted(formats, key=itemgetter('audio','ext','size')) 
	data["formats"] = sorted_formats
	
	return render_template('video.html',data=data)
  	

if __name__ == '__main__':
	# When running locally, disable OAuthlib's HTTPs verification. When
	# running in production *do not* leave this option enabled.

	app.run(debug=True)
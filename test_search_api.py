# -*- coding: utf-8 -*-

import os

import google.oauth2.credentials

import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from flask import Flask

app = Flask(__name__)
# Note: A secret key is included in the sample so that it works, but if you
# use this code in your application please replace this with a truly secret
# key. See http://flask.pocoo.org/docs/0.12/quickstart/#sessions.
app.secret_key = 'AIzaSyC778FuABmYJfUhPwa-HaY-U7xXV9ZJZnM'

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def get_authenticated_service():
	flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
	credentials = flow.run_console()
	return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

	def print_response(response):
		print(response)		


# Remove keyword arguments that are not set
def remove_empty_kwargs(**kwargs):
	good_kwargs = {}
	if kwargs is not None:
		for key, value in kwargs.iteritems():
			if value:
				good_kwargs[key] = value
				return good_kwargs

def search_list_by_keyword(client, **kwargs):
	# See full sample for function
	kwargs = remove_empty_kwargs(**kwargs)

	response = client.search().list(
		**kwargs
		).execute()

	return print_response(response)

@app.route('/')
def index():

	return "ok",200
  	

if __name__ == '__main__':
	# When running locally, disable OAuthlib's HTTPs verification. When
	# running in production *do not* leave this option enabled.
	os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
	client = get_authenticated_service()


	search_list_by_keyword(client,
			part='snippet',
			maxResults=25,
			q='surfing',
			type='')
		return "OK",200
	app.run('localhost', 5000, debug=True)
  
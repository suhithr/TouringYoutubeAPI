#!/usr/bin/python
#static folder is for stylesheets and stuff
#templates is for jinja2 html templates
from flask import Flask, render_template, url_for, request, session, redirect
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
from flask.ext.sqlalchemy import SQLAlchemy
import json
import datetime
import time

#Youtube API
DEVELOPER_KEY = "AIzaSyA8jyOIt0uwCo38aLz-5u0H0_fAKYEd288"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

#creating the application object
app = Flask(__name__)
app.config.from_object('config.ProductionConfig')

#create databse object
db = SQLAlchemy(app)

from models import *

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
	if request.method == 'POST':
		
		search_term = request.form['search_term']

		#fetching the last aka latest object from a query
		present = test.query.filter_by(term=search_term).order_by(test.id.desc()).first()
		
		#Sends API call
		def callSearchAPI(search_term):
			youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
			search_response = youtube.search().list(
				q=search_term,
				part="id, snippet",
				type="youtube#video",
				maxResults=25).execute()
			videos = []
			for search_result in search_response.get("items", []):
				videos.append({"id" : search_result["id"], "title" : search_result["snippet"]["title"]})

			time_now = datetime.datetime.now()
			#saving videos object as json object
			qry = test(search_term, json.dumps(videos), time_now)
			db.session.add(qry)
			db.session.commit()
			return videos

		#Check if it's been searched already before or not
		if present == None:
			videos = callSearchAPI(search_term)
			return render_template('search.html', search_term=search_term, videos=videos)
		else:
			diff = datetime.datetime.now() - present.time_of_search

			#It's been searched before, now check the age of the last search
			if diff.total_seconds() > 3600:
				videos = callSearchAPI(search_term)
				return render_template('search.html', search_term=search_term, videos=videos)

			videos = json.loads(present.response)
			fromDB = "It's from the database"
			return render_template('search.html', search_term=search_term, videos=videos, fromDB=fromDB)
	
	return render_template('search.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
	if request.method == 'POST':
		selected_id = request.form['selected_id']
		#Trying to retrieve the id from the existing table
		present = test_selected.query.filter_by(term_id=selected_id).order_by(test_selected.id.desc()).first()

		#Function to call the API to retrienve statistics
		def callStatAPI(selected_id):
			youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
			id_response = youtube.videos().list(
				id=selected_id,
				part='statistics').execute()

			#Assigning the values to a dictionary
			selected_video = []
			for response in id_response.get("items"):
				selected_video.append({
					"id" : selected_id, 
					"viewcount" : response["statistics"]["viewCount"], 
					"likecount" : response["statistics"]["likeCount"],
					"dislikecount" : response["statistics"]["dislikeCount"],
					"commentcount" : response["statistics"]["commentCount"],
					"favoritecount" : response["statistics"]["favoriteCount"]})

			#Inserting values into database
			time_now = datetime.datetime.now()
			qry = test_selected(selected_id, json.dumps(selected_video), time_now)
			db.session.add(qry)
			db.session.commit()
			return selected_video

		#If the data is already in the table or too old
		if present == None:
			selected_video = callStatAPI(selected_id)
			return render_template("result.html", selected_video=selected_video, selected_id=selected_id)

		else:
			#Finding out how old the data is
			diff = datetime.datetime.now() - present.time_of_request

			#If the cached data is too old
			if diff.total_seconds() > 3600:
				selected_video = callStatAPI(selected_id)
				return render_template("result.html", selected_video=selected_video, selected_id=selected_id)

			selected_video = json.loads(present.response)
			fromDB = "It's from the database"
			return render_template("result.html", selected_id=selected_id,selected_video=selected_video, fromDB=fromDB)
	return redirect(url_for('search'))


#start the server with the run method
if __name__ == '__main__':
	app.run()
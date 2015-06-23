#!/usr/bin/python
#static folder is for stylesheets and stuff
#templates is for jinja2 html templates
from flask import Flask, render_template, url_for, request, session, g
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser


#Youtube API
DEVELOPER_KEY = "AIzaSyA8jyOIt0uwCo38aLz-5u0H0_fAKYEd288"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

#creating the application object
app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
	if request.method == 'POST':
		search_term = request.form['search_term']
		
		youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
		search_response = youtube.search().list(
			q=search_term,
			part="id, snippet",
			type="youtube#video",
			maxResults=25).execute()
		videos = []
		for search_result in search_response.get("items", []):
			videos.append({"id" : search_result["id"], "title" : search_result["snippet"]["title"]})
		print videos
		return render_template('location.html', search_term=search_term, videos=videos)

	return render_template('location.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
	if request.method == 'POST':
		selected_id = request.form['selected_id']
		youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
		id_response = youtube.videos().list(
			id=selected_id,
			part='statistics').execute()
		print selected_id
		selected_video = []
		for response in id_response.get("items"):
			selected_video.append({
				"id" : selected_id, 
				"viewcount" : response["statistics"]["viewCount"], 
				"likecount" : response["statistics"]["likeCount"],
				"dislikecount" : response["statistics"]["dislikeCount"],
				"commentcount" : response["statistics"]["commentCount"],
				"favoritecount" : response["statistics"]["favoriteCount"]})
		print selected_video
		return render_template("result.html", selected_video=selected_video)
	return render_template('search.html')


#start the server with the run method
if __name__ == '__main__':
	app.run()
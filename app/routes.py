from flask import Flask, render_template, jsonify, request, g, url_for
from app import app
import random
import models

@app.route('/')
def home():
    '''creates the dict with the filepaths, and returns the template'''
    new_video()
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/_new_video')
def new_video():
    current_id = request.args.get('current_id')
    video_id = random.randrange(1,models.Video.query.count() + 1) #the +1 is to acomadate for the fact that the db starts at 1 and count is non inclusive of the highest value 
    while True:
        if video_id != current_id:
            new_video = models.Video.query.get(video_id)
            webm = new_video.get_webm()
            mp4 = new_video.get_mp4()
            return jsonify(webm=webm,mp4=mp4,video_id=video_id)

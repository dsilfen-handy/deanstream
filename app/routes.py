from flask import Flask, render_template, jsonify, session
from app import app
import random
from . import models

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
    video_list = session.get('video_list', None)
    if not video_list:
        video_list = [video.id for video in models.Video.query.all()]
        random.shuffle(video_list)
        try:
            while video_list[-1] == session['last_id']:
                random.shuffle(video_list)
        except KeyError:
            pass
    current_id = video_list.pop(0)
    if len(video_list) == 1:
        session['last_id']=current_id
    session['video_list'] = video_list
    new_video = models.Video.query.get(current_id)
    webm = new_video.get_webm()
    mp4 = new_video.get_mp4()
    return jsonify(webm=webm,mp4=mp4)

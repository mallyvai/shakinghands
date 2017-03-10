#!/usr/bin/env python

import os, json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, abort, request, jsonify, g, url_for, flash, render_template
from flask_httpauth import HTTPTokenAuth
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
import flask
import flask_login
from flask_login import login_user, LoginManager, login_required
from urlparse import urlparse, urljoin
from flask import request, url_for

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Doesn't seem to suppress warnings?

db = SQLAlchemy(app)

class Alarm(db.Model):
    __tablename__ = 'alarms'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(160)) #TODO - What shoudl this length be?
    upvotes = db.Column(db.Integer, default=0)

    @classmethod
    def add_alarm(cls, content):
        content = content.upper()
        alarm = cls(content = content)
        db.session.add(alarm)
        db.session.commit()
        return alarm
    
    @classmethod
    def get_alarms(cls):
        return cls.query.all()

    @classmethod
    def upvote_alarm(cls, alarm_id):
        alarm = Alarms.query.get(id=alarm_id)
        alarm.upvotes += 1 #TODO - Potential race condition if multiple upvoters try simultaneously.
        db.session.commit(alarm)

    def serialize(self):
        return {
            'id': self.id,
            'content': self.content,
            'upvotes': self.upvotes
        }

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        alarms = Alarm.get_alarms()
        return render_template('index.html', alarms=alarms)
    elif request.method == 'POST':
        content = request.form.get('content')
        Alarm.add_alarm(content)
        alarms = Alarm.get_alarms()
        return render_template('index.html', alarms=alarms)

@app.route('/api/alarms', methods=['POST', 'GET'])
def upvote_alarms():
    if request.method == 'POST':
        print request.json
        alarm_id = request.json.get('alarmID')
        Alarm.upvote_alarm(alarm_id)
        return "Upvoted, yay", 200

    if request.method == 'GET':
        alarms = [alarm.serialize() for alarm in Alarm.get_alarms()]
        obj = jsonify({'success': True, 'alarms': alarms})
        return obj

if __name__ == "__main__":
    if not os.path.exists('db.sqlite'):
        db.create_all()
    app.run(debug=True)


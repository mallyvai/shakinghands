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

@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')


if __name__ == "__main__":
    if not os.path.exists('db.sqlite'):
        db.create_all()
    app.run(debug=True)


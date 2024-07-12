import os
import pandas as pd
from datetime import datetime, timedelta, timezone

from flask import Flask
from flask import current_app as app
from flask import request
from flask import render_template, flash, redirect, url_for, jsonify
#from flask import Blueprint
from werkzeug.utils import secure_filename
from sqlalchemy.exc import SQLAlchemyError

#from . import db
from .models import *
from .utilities import *



############## 主要页面 ##############

@app.route('/')
def index():
    return render_template('index.html')

'''
@app.route('/<page>')
def page(page):
    return render_template(f'{page}.html')
'''

@app.route('/about')
def about():
    last_commit_time = get_last_commit_time()
    return render_template('about.html', 
                           last_update_date=last_commit_time)


@app.route('/issue')
def issue():
    return render_template('issue.html')
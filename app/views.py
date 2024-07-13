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


#main = Blueprint('main', __name__)

@app.route('/')
def home():    
    return render_template('home.html')


@app.route('/issue')
def issue():    
    return render_template('issue.html')


@app.route('/ticket')
def ticket():
    return render_template('ticket.html')


@app.route('/about')
def about():
    return render_template('about.html')
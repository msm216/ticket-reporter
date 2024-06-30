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

from . import db
#from .models import User, Group
#from .utilities import date_to_id, date_for_sqlite, allowed_file


############## 主要页面 ##############

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<page>')
def page(page):
    return render_template(f'{page}.html')
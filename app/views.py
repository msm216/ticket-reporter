import os

from flask import current_app as app
from flask import render_template, request, redirect, url_for, flash, jsonify

#from .models import Task, Ticket, Project
#from .forms import TaskForm, TicketForm, ProjectForm
#from .utilities import get_last_modified_time

from . import db


############## 主要页面 ##############

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<page>')
def page(page):
    return render_template(f'{page}.html')
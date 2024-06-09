import os

from flask import Flask
from flask import request
from flask import render_template, jsonify, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy

from app import create_app


# 通过 __init__.py 中的 create_app() 函数创建app
#app = create_app()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<page>')
def page(page):
    return render_template(f'{page}.html')


if __name__ == '__main__':
    
    app.run(debug=True)
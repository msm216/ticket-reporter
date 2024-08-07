import os
import pandas as pd

from datetime import datetime, timedelta, timezone
from flask import Flask
from flask import current_app as app
from flask import request
from flask import render_template, flash, redirect, url_for, jsonify
#from flask import Blueprint
from werkzeug.utils import secure_filename
from sqlalchemy.exc import SQLAlchemyError, OperationalError

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


@app.route('/ticket/upload', methods=['POST'])
def upload_ticket():
    # 检查请求中是否包含文件，如果不存在，显示错误信息并重定向回上传页面
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # 如果文件名为空，显示错误信息并重定向回上传页面
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    # 验证文件后缀
    if file and allowed_file(file.filename):
        # 确保上传的文件名是安全的，并移除任何可能导致安全问题的字符
        filename = secure_filename(file.filename)
        # 构建文件路径
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        # 处理文件，parse_dates 参数定义需要被转化为日期的列
        if filename.endswith('.csv'):
            df = pd.read_csv(filepath, parse_dates=['created_on'])
        elif filename.endswith('.xlsx'):
            df = pd.read_excel(filepath, parse_dates=['created_on'])
        else:
            flash('Unsupported file format')
            return redirect(request.url)

        ###
        # 对 df 的格式进行标准化处理
        ###

        # 将文件内容更新到数据库
        update_tickets_from_dataframe(df)
        flash('File successfully uploaded and processed')
        return redirect(url_for('ticket'))

    flash('File type not allowed')
    return redirect(request.url)


@app.route('/about')
def about():
    return render_template('about.html',
                           last_update_date=last_commit_time())
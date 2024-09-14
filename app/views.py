import os
import pandas as pd

from datetime import datetime, timedelta, timezone
from io import BytesIO
from weasyprint import HTML

from flask import Flask
from flask import current_app as app
from flask import request
from flask import render_template, flash, redirect, url_for, jsonify, send_file
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
    # 获取用户选择的分类标准，默认是 'none'，即不分组
    filter_by = request.args.get('filter-by', 'none')
    
    # 获取所有 Issue 实例
    issues_all = Issue.query.all()
    # 对每个 issue 的 resolutions 按照 update_on 进行降序排序
    for issue in issues_all:
        issue.resolutions = sorted(issue.resolutions, key=lambda r: r.update_on, reverse=True)
    
    issues_by_group = {}
    group_order = []
    
    # 如果用户选择了 'none'，直接展示所有 Issue，不进行分组
    if filter_by == 'none':
        group_order = ['All']
        issues_by_group = {'All': issues_all}
    # 按照 category 分组
    elif filter_by == 'category':
        categories = set([issue.category.name for issue in issues_all])
        issues_by_category = {category: [] for category in categories}
        for issue in issues_all:
            issues_by_category[issue.category.name].append(issue)
        issues_by_group = issues_by_category
        group_order = sorted(categories)  # 排序后的分类顺序
    # 按照 severity 分组
    elif filter_by == 'severity':
        severity_order = ['vital', 'critical', 'grave', 'normal', 'minor']
        issues_by_severity = {severity: [] for severity in severity_order}
        for issue in issues_all:
            severity_name = issue.severity.name
            if severity_name in issues_by_severity:
                issues_by_severity[severity_name].append(issue)
        issues_by_group = issues_by_severity
        group_order = severity_order  # 预定义好的 severity 顺序
    
    # 将分组信息和选择传递到模板
    return render_template('issue.html', 
                           issues=issues_all,
                           issues_by_group=issues_by_group, 
                           group_order=group_order,
                           filter_by=filter_by)

@app.route('/issue/print/<issue_id>', methods=['GET'])
def generate_pdf(issue_id):
    #issue_id = request.args.get('issue_id')  # POST方法用 request.form.get()
    if not issue_id:
        return "No issue selected", 400
    # 查询选择的 Issue 实例
    issue_instance = Issue.query.get(issue_id)
    if not issue_instance:
        return "Issue not found", 404
     # 渲染 HTML 模板，将 issue 实例传递给模板
    rendered_html = render_template('issue_report.html', issue=issue_instance)
    # 创建 BytesIO 对象，用于保存生成的 PDF 文件
    pdf_file = BytesIO()
    # 使用 WeasyPrint 将 HTML 转换为 PDF
    HTML(string=rendered_html).write_pdf(pdf_file)
    # 将文件指针移到文件的开始位置
    pdf_file.seek(0)
    # 返回 PDF 文件，供预览和下载
    return send_file(pdf_file, 
                     download_name=f'{issue_instance.id}.pdf', 
                     as_attachment=False, 
                     mimetype='application/pdf')


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
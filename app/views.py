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


OBJECTS = {
        'issue': Issue,
        'resolution': Resolution,
        'ticket': Ticket,
        'task': Task
    }


REFERENCE = {
        'issue': 'resolution',
        'ticket': 'task'
    }


############################################ GENERAL ROUTES ###################################################

@app.route('/')
def home():    
    return render_template('home.html')


@app.route('/load-form', methods=['GET'])
def load_form():
    # 获取请求参数 mode 的值
    mode = request.args.get('mode')
    object_type = request.args.get('objectType')
    if mode:
        return render_template(f'{object_type}/form/{mode}.html')
    else:
        return "Invalid mode", 400


@app.route('/<object_type>/<inst_id>', methods=['GET'])
def get_instance(inst_id:str, object_type:str, query:dict):
    # 根据类名获取类对象
    object = OBJECTS.get(object_type)
    # 查询指定 id 的实例
    instance = object.query.get(inst_id)

    if instance:
        return jsonify({
            'title': instance.title,
            'description': instance.description,
            # 其他字段
        })
    return jsonify({'Error': 'Instance not found'}), 404


@app.route('/<object_type>/add', methods=['POST'])
def add_instance(object_type:str):
    print(f"Adding new {object_type}...")
    return jsonify(success=True)


@app.route('/<object_type>/<inst_id>/update', methods=['POST'])
def update_instance(object_type:str, inst_id:str):
    

    print(f"Updating {object_type}: {inst_id}")


    return jsonify(success=True)


@app.route('/<object_type>/<inst_id>/delete', methods=['DELETE'])
def delete_instance(object_type, ref_id):
    print(f"Deleting {object_type}: {ref_id}")
    return jsonify(success=True)


@app.route('/<object_type>/<inst_id>/print', methods=['GET'])
def generate_pdf(inst_id:str, object_type:str):
    # 判断是否给定 id
    if not inst_id:
        return "No issue selected", 400
    # 获取模型类
    object = OBJECTS.get(object_type)
    # 查询选择的 Issue 实例
    instance = object.query.get(inst_id)
    #issue_id = request.args.get('inst_id')  # POST方法用 request.form.get()
    if not instance:
        return "Issue not found", 404
     # 渲染 HTML 模板，将 issue 实例传递给模板
    rendered_html = render_template(f'report/{object_type}.html', instance=instance)
    # 创建 BytesIO 对象，用于保存生成的 PDF 文件
    pdf_file = BytesIO()
    # 使用 WeasyPrint 将 HTML 转换为 PDF
    HTML(string=rendered_html).write_pdf(pdf_file)
    # 将文件指针移到文件的开始位置
    pdf_file.seek(0)
    # 返回 PDF 文件，供预览和下载
    return send_file(pdf_file, 
                     download_name=f'{instance.id}.pdf', 
                     as_attachment=False, 
                     mimetype='application/pdf')


############################################ ISSUE SPECIFIC ROUTES ############################################

@app.route('/issue')
def issue_page():
    
    theme = 'issue'
    print(f"Theme of the page: '{theme}'.\n")

    # 获取所有 Issue 实例
    issues_all = Issue.query.all()
    # 对每个 issue 的 resolutions 按照 update_on 进行降序排序
    for issue in issues_all:
        issue.resolutions = sorted(issue.resolutions, key=lambda r: r.update_on, reverse=True)
    
    ######## 筛选实例 ########
    start_date_str = request.args.get('start_date', '2022-01-01')
    end_date_str = request.args.get('end_date', datetime.now().strftime('%Y-%m-%d'))
    exclude_closed = request.args.get('exclude_closed', False)
    # 将日期字符串转换为日期对象
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d') + timedelta(days=1)
    # 根据日期过滤 issues
    print(f"Selecting {theme}: preported from {start_date} to {end_date}.\n")
    issues_filtered = [issue for issue in issues_all if end_date >= issue.report_on >= start_date]
    # 如果选中排除关闭状态，过滤掉状态为 "closed" 的 Issue
    if exclude_closed:
        issues_filtered = [issue for issue in issues_filtered if issue.progress.name.lower() != 'closed']
    else:
        pass
    #########################

    ######## 分组显示实例 ########
    issues_by_group = {'All': issues_filtered}
    group_order = ['All']
    # 获取用户选择的分类标准，默认不分组
    filter_by = request.args.get('filter-by', 'none')
    if filter_by == 'none':
        group_order = ['All']
        issues_by_group = {'All': issues_filtered}
    elif filter_by == 'category':
        categories = set([issue.category.name for issue in issues_filtered])
        issues_by_category = {category: [] for category in categories}
        for issue in issues_filtered:
            issues_by_category[issue.category.name].append(issue)
        issues_by_group = issues_by_category
        group_order = sorted(categories)  # 排序后的分类顺序
    elif filter_by == 'severity':
        severity_order = ['vital', 'critical', 'grave', 'normal', 'minor']
        issues_by_severity = {severity: [] for severity in severity_order}
        for issue in issues_filtered:
            severity_name = issue.severity.name
            if severity_name in issues_by_severity:
                issues_by_severity[severity_name].append(issue)
        issues_by_group = issues_by_severity
        group_order = severity_order
    #############################

    return render_template('issue/page.html', 
                           page_theme=theme,
                           issues=issues_all,
                           issues_by_group=issues_by_group, 
                           group_order=group_order,
                           filter_by=filter_by,
                           default_start_date=start_date_str,
                           default_end_date=end_date_str
                           )



############################################ TICKET SPECIFIC ROUTES ###########################################

@app.route('/ticket')
def ticket_page():

    theme = 'ticket'
    print(f"Theme of the page: '{theme}'.\n")

    # 获取所有 Issue 实例
    tickets_all = Ticket.query.all()
    # 对每个 issue 的 resolutions 按照 update_on 进行降序排序
    for ticket in tickets_all:
        ticket.resolutions = sorted(ticket.resolutions, key=lambda r: r.update_on, reverse=True)

    return render_template('ticket/page.html',
                           tickets=tickets_all
                           )


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


############################################ SERVICE SPECIFIC ROUTES ##########################################

@app.route('/service')
def service_page():
    return render_template('service/page.html'
                           )


############################################ ABOUT SPECIFIC ROUTES ############################################

@app.route('/about')
def about_page():
    return render_template('about.html',
                           last_update_date=last_commit_time())
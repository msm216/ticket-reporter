import os
import pandas as pd

from datetime import datetime, timedelta, timezone
from io import BytesIO
from weasyprint import HTML

from flask import Flask
from flask import current_app
from flask import request
from flask import render_template, flash, redirect, url_for, jsonify, send_file
from flask import Blueprint
from werkzeug.utils import secure_filename
from sqlalchemy.exc import SQLAlchemyError, OperationalError

from . import db
from .models import *
from .utilities import *


bp = Blueprint('main', __name__)


MODELS = {
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

@bp.route('/')
def home():    
    return render_template('home.html')


@bp.route('/load-form', methods=['GET'])
def load_form():
    # 获取请求参数 mode 的值
    mode = request.args.get('modal-mode')
    object_class = request.args.get('object-class')
    print(f"Loading form '{mode}' for page '{object_class}'...")
    today = datetime.now().strftime('%Y-%m-%d')
    if mode:
        # issue/form/add.html
        return render_template(f'{object_class}/form/{mode}.html', today=today)
    else:
        return "Invalid mode", 400


@bp.route('/<object_class>/<inst_id>', methods=['GET'])
def get_instance(inst_id:str, object_class:str):
    print(f"Getting {object_class}: {inst_id}...")
    # 根据类名获取类对象
    object_model = MODELS.get(object_class)
    if not object_model:
        return jsonify({'Error': f'Model {object_class} not found'}), 404
    # 查询指定 id 的实例
    instance = object_model.query.get(inst_id)
    if instance:
        # 动态获取模型实例的所有属性值
        instance_data = {}
        for column in object_model.__table__.columns:
            value = getattr(instance, column.name)
            if isinstance(value, enum.Enum):  # 如果是枚举，取其值
                instance_data[column.name] = value.value
            elif isinstance(value, datetime):  # 如果是日期，转化为字符串
                instance_data[column.name] = value.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(value, (str, int, float, bool, type(None))):
                instance_data[column.name] = value
            else:
                instance_data[column.name] = str(value)
        return jsonify(instance_data)
    return jsonify({'Error': 'Instance not found'}), 404


# 添加新实例
@bp.route('/<object_class>/add', methods=['POST'])
def add_instance(object_class:str):
    print(f"Adding new {object_class}...")
    # 根据类名获取类对象
    object_model = MODELS.get(object_class)
    if not object_model:
        return jsonify(success=False, message=f"Model {object_class} not exist"), 400
    try:
        # 通过请求头区分数据获取方式
        if request.content_type == 'application/json':
            form_data = request.json  # 获取 JSON 数据
        else:
            form_data = request.form.to_dict()   # 用于接收传统的表单提交
        print(f"Received form data for '{object_class}': {form_data}")
        # 如果没有提供 report_o，则使用当前日期
        report_on = form_data.get('report_on')
        if not report_on:
            form_data['report_on'] = datetime.now()
        else:
            form_data['report_on'] = datetime.strptime(report_on, '%Y-%m-%d')
        # 过滤无效字段，仅保留模型定义的字段
        valid_fields = {key: form_data[key] for key in form_data if key in object_model.__table__.columns.keys()}
        # 创建新的模型实例，将表单数据传入
        new_instance = object_model(**valid_fields)
        # 添加到数据库会话中并提交
        db.session.add(new_instance)
        db.session.commit()
        # 返回成功的 JSON 响应
        return jsonify(success=True, id=new_instance.id)
    except Exception as e:
        # 如果发生错误，回滚事务
        db.session.rollback()  
        print(f"Error adding {object_class}: {str(e)}")
        # 返回失败的 JSON 响应
        return jsonify(success=False, message=f"Failed to add instance: {str(e)}"), 500


# 修改现有实例
@bp.route('/<object_class>/<inst_id>/edit', methods=['PUT'])
def edit_instance(object_class: str, inst_id: int):
    print(f"Editing {object_class} instance: {inst_id}...")
    # 根据类名获取类对象
    object_model = MODELS.get(object_class)
    if not object_model:
        return jsonify(success=False, message=f"Model {object_class} not exist"), 400
    try:
        # 通过请求头区分数据获取方式
        if request.content_type == 'application/json':
            form_data = request.json  # 获取 JSON 数据
        else:
            form_data = request.form.to_dict()  # 用于接收传统的表单提交
        print(f"Received form data for '{object_class}': {form_data}")
        # 查询数据库中的实例
        instance = object_model.query.get(inst_id)
        if not instance:
            return jsonify(success=False, message=f"{object_class} instance with ID {inst_id} not found"), 404
        # 更新实例的属性
        for key, value in form_data.items():
            if key in object_model.__table__.columns.keys():
                setattr(instance, key, value)
        # 提交数据库更新
        db.session.commit()
        return jsonify(success=True, message="Instance updated successfully")
    except Exception as e:
        db.session.rollback()  # 如果发生错误，回滚事务
        print(f"Error updating {object_class}: {str(e)}")
        return jsonify(success=False, message="Failed to update instance: " + str(e)), 500


@bp.route('/<object_class>/<inst_id>/update', methods=['POST'])
def update_instance(object_class:str, inst_id:str):
    print(f"Updating {object_class}: {inst_id}")

    return jsonify(success=True)


@bp.route('/<object_class>/<inst_id>/delete', methods=['DELETE'])
def delete_instance(object_class:str, inst_id:str):
    print(f"Deleting {object_class}: {inst_id}")
    # 根据类名获取类对象
    object_model = MODELS.get(object_class)
    # 根据 id 查询实例
    instance = object_model.query.get(inst_id)
    db.session.delete(instance)
    db.session.commit()
    return jsonify(success=True)

# 打印指定实例的 PDF 报告
@bp.route('/<object_class>/<inst_id>/print', methods=['GET'])
def generate_pdf(inst_id:str, object_class:str):
    # 判断是否给定 id
    if not inst_id:
        return "No issue selected", 400
    # 获取模型类
    object_model = MODELS.get(object_class)
    # 查询选择的 Issue 实例
    instance = object_model.query.get(inst_id)
    #issue_id = request.args.get('inst_id')  # POST方法用 request.form.get()
    if not instance:
        return "Issue not found", 404
     # 渲染 HTML 模板，将 issue 实例传递给模板
    rendered_html = render_template(f'report/{object_class}.html', inst=instance)
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

@bp.route('/issue')
def issue_page():
    
    theme = 'issue'
    print(f"\nPage theme: {theme}")
    print("\nPage requests:".join([f"{key}: {value}" for key, value in request.args.items()]))

    # 获取所有 Issue 实例
    issues_all = Issue.query.all()
    # 对每个 issue 的 resolutions 按照 update_on 进行降序排序
    for issue in issues_all:
        issue.resolutions = sorted(issue.resolutions, key=lambda r: r.update_on, reverse=True)
    
    ######## 处理实例选择 ########
    selected_issue_id = request.args.get('issue-select', 'all')
    
    if selected_issue_id == 'all':
        # 如果未选择特定实例，则应用其他筛选条件
        start_date_str = request.args.get('start-date', '2024-01-01')
        end_date_str = request.args.get('end-date', datetime.now().strftime('%Y-%m-%d'))
        exclude_closed = request.args.get('exclude-closed', False)
        # 将日期字符串转换为日期对象
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d') + timedelta(days=1)
        # 根据日期过滤 issues
        issues_filtered = [issue for issue in issues_all if end_date >= issue.report_on >= start_date]
        ######## 筛除已关闭实例 #########
        if exclude_closed:
            issues_filtered = [issue for issue in issues_filtered if issue.progress.name.lower() != 'closed']
        else:
            pass
        ######## 处理分组显示实例 ########
        # 获取用户选择的分类标准，默认不分组
        grouping_by = request.args.get('grouping-by', 'none')
        if grouping_by == 'none':
            issues_by_group = {'All': issues_filtered}
            group_order = ['All']
        elif grouping_by == 'category':
            categories = set([issue.category.name for issue in issues_filtered])
            issues_by_category = {category: [] for category in categories}
            for issue in issues_filtered:
                issues_by_category[issue.category.name].append(issue)
            issues_by_group = issues_by_category
            group_order = sorted(categories)  # 排序后的分类顺序
        elif grouping_by == 'severity':
            severity_order = ['vital', 'critical', 'grave', 'normal', 'minor']
            issues_by_severity = {severity: [] for severity in severity_order}
            for issue in issues_filtered:
                severity_name = issue.severity.name
                if severity_name in issues_by_severity:
                    issues_by_severity[severity_name].append(issue)
            issues_by_group = issues_by_severity
            group_order = severity_order
        ###################################
        expanded_issue_id = None
    else:
        # 如果选择了特定的实例，只显示这个实例，忽略其他筛选条件
        selected_issue = next((issue for issue in issues_all if issue.id == selected_issue_id), None)
        # 重置筛选参数的值
        issues_by_group = {'Selected': [selected_issue]}
        group_order = ['Selected']
        grouping_by = 'none'
        start_date_str = '2024-01-01'
        end_date_str = datetime.now().strftime('%Y-%m-%d')
        ###################################
        expanded_issue_id = selected_issue_id
        
    return render_template('issue/page.html', 
                           page_theme=theme,
                           issues=issues_all,
                           issues_by_group=issues_by_group, 
                           group_order=group_order,
                           grouping_by=grouping_by,
                           default_start_date=start_date_str,
                           default_end_date=end_date_str,
                           expanded_issue_id=expanded_issue_id
                           )



############################################ TICKET SPECIFIC ROUTES ###########################################

@bp.route('/ticket')
def ticket_page():

    theme = 'ticket'
    print(f"\nTheme of the page: '{theme}'.")

    # 获取所有 Issue 实例
    tickets_all = Ticket.query.all()
    # 对每个 issue 的 resolutions 按照 update_on 进行降序排序
    for ticket in tickets_all:
        ticket.tasks = sorted(ticket.tasks, key=lambda r: r.execute_on, reverse=True)

    tickets_filtered = tickets_all

    ######## 分组显示实例 ########
    tickets_by_group = {'All': tickets_filtered}
    group_order = ['All']
    # 获取用户选择的分类标准，默认不分组
    #filter_by = request.args.get('filterBy', 'none')
    filter_by = 'none'
    #############################

    return render_template('ticket/page.html',
                           tickets=tickets_all,
                           tickets_by_group=tickets_by_group, 
                           group_order=group_order,
                           filter_by=filter_by,
                           )


@bp.route('/ticket/upload', methods=['POST'])
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
        filepath = os.path.join(bp.config['UPLOAD_FOLDER'], filename)
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


########################################## COMMISSION SPECIFIC ROUTES #########################################

@bp.route('/commission')
def commission_page():

    theme = 'commission'
    print(f"\nTheme of the page: '{theme}'.")

    return render_template('commission/page.html'
                           )


############################################ SERVICE SPECIFIC ROUTES ##########################################

@bp.route('/service')
def service_page():

    theme = 'service'
    print(f"\nTheme of the page: '{theme}'.")

    return render_template('service/page.html'
                           )


############################################ ABOUT SPECIFIC ROUTES ############################################

@bp.route('/about')
def about_page():

    theme = 'about'
    print(f"\nTheme of the page: '{theme}'.")

    return render_template('about.html',
                           last_update_date=last_commit_time())